import pyzipper as pz
import os
import logging

logger = logging.getLogger(__name__)

def compress_file(file_path, target_path, password) -> None:
    logger.info(f"Starting compression for: {file_path}")
    try:
        with pz.AESZipFile(target_path, 'w',
                           compression=pz.ZIP_LZMA,
                           encryption=pz.WZ_AES) as zf:
            zf.setpassword(password.encode())
            zf.write(file_path, arcname=os.path.basename(file_path))
        logger.info(f"Compression success: {target_path}")
    except Exception as e:
        logger.error(f"Compression failed: {e}")
        raise SystemExit(1)

def decompress_file(file_path, target_path, password) -> None:
    logger.info(f"Starting decompression for: {file_path}")
    try:
        with pz.AESZipFile(file_path, 'r',
                           compression=pz.ZIP_LZMA,
                           encryption=pz.WZ_AES) as zf:
            zf.setpassword(password.encode())
            zf.extractall(target_path)
        logger.info(f"Decompression success: {file_path}")
    except Exception as e:
        logger.error(f"Decompression failed: {e}")
        raise SystemExit(1)