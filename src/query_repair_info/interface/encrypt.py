from cryptography.fernet import Fernet
import logging
from query_repair_info.bootstrap import BASE_DIR

AES_KEY = BASE_DIR / "config" / "aes.key"
logger  = logging.getLogger(__name__)

def encrypt_file(file_path, target_path) -> None:
    logger.info(f"Starting encryption for {file_path} to {target_path}")
    try:
        with open(AES_KEY, 'rb') as f:
            aes_key = f.read()
        fernet = Fernet(aes_key)
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(target_path, 'wb') as f:
            f.write(encrypted)
        logger.info(f"Encryption success: {target_path}")
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise SystemExit(1)
    
def decrypt_file(file_path, target_path) -> None:
    logger.info(f"Starting decryption for {file_path} to {target_path}")
    try:
        with open(AES_KEY, 'rb') as f:
            aes_key = f.read()
        fernet = Fernet(aes_key)
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(target_path, 'wb') as f:
            f.write(decrypted_data)
        logger.info(f"Decryption success: {target_path}")
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        raise SystemExit(1)