from pathlib import Path
from .validator import SUPPORTED_FORMATS


def resolve_inputs(path: str) -> list:
    p = Path(path)

    if p.is_file():
        return [str(p)]

    if p.is_dir():
        return sorted(
            str(f)
            for f in p.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS
        )

    raise FileNotFoundError(f"Path not found: {path}")
