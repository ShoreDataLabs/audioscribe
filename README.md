# Audio Transcription

A local CLI tool that transcribes audio files to clean, structured text using [OpenAI Whisper](https://github.com/openai/whisper). Runs entirely offline — no API keys, no cloud, no cost per minute.

## Features

- Transcribes any common audio format (`.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`, `.aac`, `.wma`)
- Outputs structured `.txt` files with timestamps, metadata header, and wrapped lines
- Batch mode — process an entire folder in one command
- Auto-detects language or accepts a language hint for faster processing
- Supports all Whisper model sizes (`tiny` → `large`)
- Fully tested — 47 unit tests, no heavy dependencies required to run the test suite

## Example Output

```
========================================
 TRANSCRIPTION
========================================
 File     : recording.mp3
 Date     : 2026-03-30
 Duration : 42:02
 Language : en
 Model    : whisper-medium
========================================

[00:00:00] So this system basically drops to the critical risk
           for real time.

[00:00:03] So this system will have three components.

[00:00:06] It has the data ingestion layer.

...

========================================
 END OF TRANSCRIPTION
========================================
```

## Requirements

- Python 3.9+
- [ffmpeg](https://ffmpeg.org/) installed on your system

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/ShoreDataLabs/audioscribe.git
cd audioscribe

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install ffmpeg (macOS)
brew install ffmpeg

# Install ffmpeg (Ubuntu/Debian)
# sudo apt install ffmpeg

# Install ffmpeg (Windows)
# https://ffmpeg.org/download.html
```

## Usage

### Transcribe a single file

```bash
python transcribe.py audio/recording.mp3
```

### Transcribe a whole folder

```bash
python transcribe.py audio/ --batch
```

### Options

```
positional arguments:
  path                  Path to an audio file, or a directory when using --batch

options:
  --batch               Process all audio files found in the given directory
  --model {tiny,base,small,medium,large}
                        Whisper model size (default: medium)
  --output OUTPUT       Output directory for transcript files (default: ./output)
  --language LANGUAGE   Language code e.g. 'en' or 'fr' (default: auto-detect)
```

### Examples

```bash
# Use a larger model for better accuracy
python transcribe.py recording.mp3 --model large

# Skip language detection for faster processing
python transcribe.py recording.mp3 --language en

# Batch transcribe with custom output directory
python transcribe.py recordings/ --batch --output ./transcripts
```

## Model Size Guide

| Model  | Size   | Speed  | Accuracy | Best For                        |
|--------|--------|--------|----------|---------------------------------|
| tiny   | 75 MB  | Fastest | Good    | Quick drafts, clear audio       |
| base   | 145 MB | Fast   | Better   | General use                     |
| small  | 465 MB | Medium | Good     | Balanced                        |
| medium | 1.5 GB | Slower | Great    | Default — best general accuracy |
| large  | 2.9 GB | Slowest | Best    | Maximum accuracy, long-form     |

The model is downloaded automatically on first use and cached locally.

## Project Structure

```
audio-transcription/
├── transcribe.py          # CLI entry point
├── src/
│   ├── validator.py       # File format, existence, and size checks
│   ├── input_handler.py   # Single file and batch directory resolution
│   ├── preprocessor.py    # ffmpeg conversion to 16kHz mono WAV
│   ├── engine.py          # Whisper wrapper with lazy model caching
│   ├── formatter.py       # Structured transcript output with timestamps
│   └── writer.py          # Writes output file, creates directories
├── specs/                 # Acceptance criteria per module
├── tests/                 # 47 unit tests (pytest)
└── output/                # Default transcript output directory (gitignored)
```

## Running Tests

No heavy dependencies needed — Whisper and ffmpeg are fully mocked.

```bash
pip install pytest
python -m pytest tests/ -v
```

## License

MIT
