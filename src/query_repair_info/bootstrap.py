import os
import sys
from pathlib import Path

def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(os.path.dirname(sys.executable))
    else:
        return Path(os.path.dirname(os.path.abspath(__file__)).rsplit(os.sep, 2)[0])

BASE_DIR : Path = _base_dir()