from pathlib import Path


def write_transcript(content: str, input_path: str, output_dir: str) -> str:
    stem = Path(input_path).stem
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{stem}.txt"
    out_file.write_text(content, encoding="utf-8")
    return str(out_file)
