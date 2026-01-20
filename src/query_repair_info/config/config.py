import tomllib
from time import strftime, localtime
import os
from query_repair_info.bootstrap import BASE_DIR

CONFIG_PATH = BASE_DIR / "config" / "config.toml"

class Config:
    def __init__(self) -> None:
        if not CONFIG_PATH.exists():
            raise FileNotFoundError(f"Configuration file not found at {CONFIG_PATH}")

        with open(CONFIG_PATH, "rb") as f:
            self._data = tomllib.load(f)

    @property
    def database(self) -> dict:
        return self._data.get("DataBase", {})
    
    @property
    def query_columns(self) -> list[str]:
        return self._data.get("QueryColumns", {}).get("columns", [])
    
    @property
    def maintenance_scenario(self) -> dict[int, str]:
        raw = self._data.get("MaintenanceScenario", {})
        return {int(k): v for k, v in raw.items()}

    @property
    def maintenance_strategy(self) -> dict[int, str]:
        raw = self._data.get("MaintenanceStrategy", {})
        return {int(k): v for k, v in raw.items()}
    
    @property
    def solution(self) -> list[str]:
        return self._data.get("Solutions", {}).get("patterns", [])
    
    @property
    def responsibility(self) -> dict[int, str]:
        raw = self._data.get("Responsibility", {})
        return {int(k): v for k, v in raw.items()}
    
    @property
    def file_name(self) -> str:
        return self._data.get("Paths", {}).get("file_name", "修理情報.xlsx")
    
    @property
    def query_result_save_path(self) -> str:
        query_result_save_path = self._data.get("Paths", {}).get("query_result_save_path", "")
        if not os.path.exists(query_result_save_path):
            os.makedirs(query_result_save_path)
        return query_result_save_path
    
    @property
    def compress_file_save_path(self) -> str:
        return self._data.get("Paths", {}).get("compress_file_save_path", self.query_result_save_path)
    
    @property
    def encrypt_file_save_path(self) -> str:
        return self._data.get("Paths", {}).get("encrypt_file_save_path", self.query_result_save_path)
    
    @property
    def download_file_save_path(self) -> str:
        download_file_save_path = self._data.get("Paths", {}).get("download_file_save_path", "")
        if not os.path.exists(download_file_save_path):
            os.makedirs(download_file_save_path)
        return download_file_save_path
    
    @property
    def decompress_file_save_path(self) -> str:
        return self._data.get("Paths", {}).get("decompress_file_save_path", self.download_file_save_path)
    
    @property
    def decrypt_file_save_path(self) -> str:
        return self._data.get("Paths", {}).get("decrypt_file_save_path", self.download_file_save_path)
    
    @property
    def log_dir(self) -> str:
        log_dir = self._data.get("Paths", {}).get("log_dir", BASE_DIR / "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir
    
    @property
    def save_method(self) -> int:
        return self._data.get("Others", {}).get("save_method", 1)

    @property
    def boxpath(self) -> str:
        return self._data.get("Others", {}).get("boxpath", "")
    
    @property
    def query_date(self) -> str:
        if self._data.get("Others", {}).get("query_date", "") == "":
            return strftime("%Y-%m-%d", localtime())
        else:
            return self._data.get("Others", {}).get("query_date") 

config = Config()