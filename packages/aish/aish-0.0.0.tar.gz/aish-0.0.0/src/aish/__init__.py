from pathlib import Path
import platform
import sys


PACKAGE_NAME = Path(__file__).parent.name
VERSION = "0.0.0"
EXECUTABLE_NAME = PACKAGE_NAME

if platform.system() == "Windows":
    import os
    appdata = os.getenv("LOCALAPPDATA")
    DATA_DIR = Path(appdata) / PACKAGE_NAME
else:
    DATA_DIR = Path.home() / ".local" / "share" / PACKAGE_NAME

try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except OSError as e:
    print(f"Error while attempting to create data directory: {e}")
    sys.exit(1)






