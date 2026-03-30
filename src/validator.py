from pathlib import Path

SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma"}
MAX_FILE_SIZE_BYTES = 500 * 1024 * 1024  # 500MB


def validate(path: str, batch: bool = False) -> bool:
    p = Path(path)

    if batch:
        if not p.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")
        return True

    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if p.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {p.suffix!r}. Supported: {sorted(SUPPORTED_FORMATS)}")

    if p.stat().st_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"File too large: {path} (max 500MB)")

    return True
