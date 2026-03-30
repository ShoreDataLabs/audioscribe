import pytest
from pathlib import Path


@pytest.fixture
def tmp_wav_file(tmp_path):
    f = tmp_path / "sample.wav"
    f.write_bytes(b"RIFF" + b"\x00" * 100)
    return str(f)


@pytest.fixture
def tmp_mp3_file(tmp_path):
    f = tmp_path / "sample.mp3"
    f.write_bytes(b"\xff\xfb" + b"\x00" * 100)
    return str(f)


@pytest.fixture
def sample_segments():
    return [
        {"start": 0.0, "end": 5.2, "text": "Hello and welcome to the podcast."},
        {"start": 5.2, "end": 12.8, "text": "Today we are going to talk about audio transcription."},
        {
            "start": 12.8,
            "end": 20.0,
            "text": (
                "This is a very long sentence that should be wrapped when it "
                "exceeds the line width limit of seventy characters total."
            ),
        },
    ]


@pytest.fixture
def sample_metadata():
    return {
        "filename": "interview.mp3",
        "date": "2026-03-30",
        "duration": 20.0,
        "language": "en",
        "model": "medium",
    }


@pytest.fixture
def whisper_result(sample_segments):
    return {
        "text": " ".join(s["text"] for s in sample_segments),
        "segments": [
            {
                "id": i,
                "start": s["start"],
                "end": s["end"],
                "text": s["text"],
                "tokens": [],
                "temperature": 0.0,
                "avg_logprob": -0.2,
                "compression_ratio": 1.2,
                "no_speech_prob": 0.01,
            }
            for i, s in enumerate(sample_segments)
        ],
        "language": "en",
    }
