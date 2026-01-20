from query_repair_info.config.config import config
from query_repair_info.interface.logging_config import setup_logging
from query_repair_info.interface.encrypt import decrypt_file
from query_repair_info.interface.compress import decompress_file
from query_repair_info.utils.drive_method import download_file
from time import strftime, localtime, sleep
import logging
import shutil

def download_and_decrypt():
    setup_logging(log_dir=config.log_dir, log_file="download.log")
    logger = logging.getLogger(__name__)
    logger.info("Starting download and decrypt process...")
    
    try:
        target_download_path = f"{config.download_file_save_path}"
        target_decompress_path = f"{config.decompress_file_save_path}/{config.file_name}.zip"
        target_decrypt_path = f"{config.decrypt_file_save_path}/{config.file_name}.xlsx"
        
        current_year_month = strftime("%Y%m", localtime())
        
        box_path = config.boxpath
        
        while download_file(f'{config.file_name}.enc', f"{target_download_path}/{config.file_name}.enc") == 0:
            logger.info("File not available yet. Waiting for the next check...")    
            for remaining in range(60, 0, -1):
                print(f"\rNext check in {remaining} seconds...", end="", flush=True)
                sleep(1)

        decrypt_file(f"{target_download_path}/{config.file_name}.enc", target_decompress_path)
        decompress_file(target_decompress_path, target_download_path, current_year_month)

        logger.info(f"Copying from {target_decrypt_path} \n to {box_path}...")
        shutil.copy2(target_decrypt_path, box_path)
    
        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"Process failed: {e}")
        raise SystemExit(1)
    

if __name__ == "__main__":
    download_and_decrypt()