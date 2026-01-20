import subprocess
from pathlib import Path

APP_NAME = "QueryRepairInfo"
COMPANY_NAME = "CPSpeed"

def get_git_tag():
    try:
        tag = subprocess.check_output(
            ["git", "describe", "--tags"], stderr=subprocess.STDOUT).strip().decode()
        return tag.lstrip('v')
    except subprocess.CalledProcessError:
        return "0.0.0"
    
def to_file_version(ver: str) -> str:
    parts = ver.split('.')
    while len(parts) < 4:
        parts.append('0')
    return ', '.join(parts[:4])

version = get_git_tag()

template = Path("version.template.txt").read_text(encoding="utf-8")

content = (
    template
    .replace("{APP_NAME}", APP_NAME)
    .replace("{COMPANY_NAME}", COMPANY_NAME)
    .replace("{VER_STR}", f"v{version}")
    .replace("{FILE_VER}", to_file_version(version))
)

Path("version.txt").write_text(content, encoding="utf-8")

Path("version.py").write_text(
    f'__version__ = "{version}"\n',
    encoding="utf-8"
    )

print(f"Version generated: V{version}")