from . import DATA_DIR


_KEY_FILE = DATA_DIR / "api_key"
if not _KEY_FILE.exists():
    _KEY_FILE.touch()


def load_key() -> str:
    return _KEY_FILE.read_text()


def save_key(key: str):
    _KEY_FILE.write_text(key)

