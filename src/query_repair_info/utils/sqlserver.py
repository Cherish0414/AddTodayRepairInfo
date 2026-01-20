from pandas import DataFrame
from ..interface.sqlserver_conn import db_connection
from ..config.config import config
import logging

logger = logging.getLogger(__name__)

def query_testdata() -> DataFrame:
    query_columns = ', '.join([f"{col}" for col in config.query_columns])
    query_columns_a = ", ".join([f"R.{col}" for col in config.query_columns])
    query_columns_s = ", ".join([f"S.{col}" for col in config.query_columns])
    query_date = config.query_date

    query = f"""
        WITH RecursiveCTE AS (
            SELECT 
                IMEI_Main   AS StartIMEI,
                IMEI_Main   AS CurrentIMEI,
                {query_columns},
                0           AS Level,
                BSN,
                BSN2
            FROM [CPS-PL-Database].dbo.TestData
            WHERE RR_TestTimes > '{query_date}'
            UNION ALL
            SELECT 
                R.StartIMEI,
                T.IMEI_Main,
                {query_columns_a},
                R.Level + 1,
                T.BSN,
                T.BSN2
            FROM [CPS-PL-Database].dbo.TestData AS T
            INNER JOIN RecursiveCTE AS R
                ON R.BSN2 = T.BSN
        ),
        Marks AS (
            SELECT
                *,
                ROW_NUMBER() OVER (PARTITION BY StartIMEI ORDER BY Level ASC)  AS rn_start,
                ROW_NUMBER() OVER (PARTITION BY StartIMEI ORDER BY Level DESC) AS rn_end
            FROM RecursiveCTE
        )
        SELECT
            S.StartIMEI,
            {query_columns_s},
            E.CurrentIMEI AS EndIMEI
        FROM Marks AS S
        JOIN Marks AS E
        ON E.StartIMEI = S.StartIMEI
        WHERE S.rn_start = 1
        AND E.rn_end   = 1
        ORDER BY S.RR_TestTimes;
    """
    
    with db_connection() as conn:
        df = DataFrame.from_records(
            conn.execute(query).fetchall(),
            columns=[column[0] for column in conn.execute(query).description]
        )
    logger.info(f"Retrieved {len(df)} records from the database.")
    return df