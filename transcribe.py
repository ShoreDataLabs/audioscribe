#!/usr/bin/env python3
import argparse
import sys
from datetime import date
from pathlib import Path

from src.input_handler import resolve_inputs
from src.validator import validate
from src.preprocessor import preprocess
from src.engine import TranscriptionEngine
from src.formatter import format_transcript
from src.writer import write_transcript


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files to structured text files."
    )
    parser.add_argument(
        "path",
        help="Path to an audio file, or a directory when using --batch",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all audio files found in the given directory",
    )
    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: medium)",
    )
    parser.add_argument(
        "--output",
        default="./output",
        help="Output directory for transcript files (default: ./output)",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Language code, e.g. 'en' or 'fr' (default: auto-detect)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    validate(args.path, batch=args.batch)
    files = resolve_inputs(args.path)

    if not files:
        print("No audio files found.", file=sys.stderr)
        sys.exit(1)

    engine = TranscriptionEngine(model_size=args.model)
    print(f"Loading whisper-{args.model} model...")

    for audio_path in files:
        print(f"\nTranscribing: {Path(audio_path).name}")

        wav_path = preprocess(audio_path)
        result = engine.transcribe(wav_path, language=args.language)

        metadata = {
            "filename": Path(audio_path).name,
            "date": str(date.today()),
            "duration": result["duration"],
            "language": result["language"],
            "model": args.model,
        }

        content = format_transcript(metadata, result["segments"])
        output_path = write_transcript(content, audio_path, args.output)
        print(f"  → {output_path}")

    print(f"\nDone. {len(files)} file(s) transcribed.")


if __name__ == "__main__":
    main()
