from query_repair_info.config.config import config
from query_repair_info.interface.logging_config import setup_logging
from query_repair_info.interface.encrypt import encrypt_file
from query_repair_info.interface.compress import compress_file
from query_repair_info.utils.sqlserver import query_testdata
from query_repair_info.utils.fix_data_by_df import fix_data
from query_repair_info.utils.write2excel_from_df import write_df_to_excel
from query_repair_info.utils.append2excel_from_df import append_df_to_excel
from query_repair_info.utils.format_excel import format_sheet
from query_repair_info.utils.drive_method import upload_or_update
from time import strftime, localtime
import logging

logger = logging.getLogger(__name__)

def query_and_upload():

    try:       
        setup_logging(log_dir=config.log_dir, log_file="upload.log")
        logger = logging.getLogger(__name__)
        logger.info("Starting query and upload process...")
        
        file_path = f"{config.query_result_save_path}/{config.file_name}.xlsx"
        target_compress_path = f"{config.compress_file_save_path}/{config.file_name}.zip"
        target_encrypt_path = f"{config.encrypt_file_save_path}/{config.file_name}.enc"
        
        current_year = strftime("%Y", localtime())
        current_month = strftime("%m", localtime())
        current_year_month = strftime("%Y%m", localtime())
        sheet_name = f'{current_year}年{current_month}月'
        
        save_method = config.save_method
        
        df = query_testdata()
        df_fixed = fix_data(df)
        
        if save_method == 0:
            write_df_to_excel(df_fixed, file_path, sheet_name)
            
        elif save_method == 1:
            append_df_to_excel(df_fixed, file_path, sheet_name)
            format_sheet(file_path, sheet_name)
        
        else:
            logger.error("Invalid save_method in config. Use 0 for write, 1 for append.")
            raise SystemExit(1)
        
        compress_file(file_path, target_compress_path,current_year_month)
        encrypt_file(target_compress_path, target_encrypt_path)
        upload_or_update(target_encrypt_path, f'{config.file_name}.enc')
        logger.info("Process completed successfully.")
    
    except Exception as e:
        logger.error(f"Process failed: {e}")
        raise SystemExit(e)

if __name__ == "__main__":
    query_and_upload()