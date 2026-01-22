import pandas as pd
from ..config.config import config
import logging

logger = logging.getLogger(__name__)

def move_imei_column(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {'修理前IMEI', '修理後IMEI'}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"缺少必要列: {missing}")

    df['修理前IMEI'] = df['修理前IMEI'].fillna(df['修理後IMEI'])

    mask_same = df['修理前IMEI'] == df['修理後IMEI']
    df.loc[mask_same, '修理後IMEI'] = None

    col = df.pop('修理前IMEI')
    df.insert(0, '修理前IMEI', col)

    return df

def expand_repair_methods_static(df, column='修理手段', mark='〇') -> pd.DataFrame:
    patterns = config.solution
    
    for pattern in patterns + ['その他']:
        df[pattern] = ''

    for idx, value in df[column].fillna('').astype(str).items():
        found_patterns = []
        for pattern in patterns:
            if pattern in value:
                df.at[idx, pattern] = mark
                found_patterns.append(pattern)

        extra = [v.strip() for v in value.split(';') if v.strip() and v.strip() not in found_patterns]
        if extra:
            df.at[idx, 'その他'] = ';'.join(extra)

    return df.drop(columns=[column])

def fix_data(df:pd.DataFrame) -> pd.DataFrame:
    df.rename(
        columns=
        {
            'IMEI_Main_Current' : '修理後IMEI',
            'RR_TestTimes' : '修理報告時間',
            'ManagementNumber' : '管理番号',
            'MaintenanceScenario' : '修理パターン',
            'MaintenanceStrategy' : '修理方針',
            'RootCause' : '不具合の症状',
            'Solutions' : '修理手段',
            'responsibilitydivision' : '責任',
            'IMEI_Main_Original' : '修理前IMEI',
        }, inplace=True
    )
    
    df['修理報告時間'] = pd.to_datetime(df['修理報告時間'])
    df['修理報告時間'] = df['修理報告時間'].dt.strftime('%Y/%m/%d %H:%M:%S')
    df['修理パターン'] = df['修理パターン'].replace(config.maintenance_scenario)
    df['修理方針'] = df['修理方針'].replace(config.maintenance_strategy)
    df['責任'] = df['責任'].replace(config.responsibility)
    df = expand_repair_methods_static(df)
    df = move_imei_column(df)

    logger.info("DataFrame Fixed")
    
    return df