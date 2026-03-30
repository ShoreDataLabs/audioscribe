import pytest
from pathlib import Path
from src.writer import write_transcript


class TestWriteTranscript:
    def test_output_filename_mirrors_input_with_txt_extension(self, tmp_path, tmp_mp3_file):
        # AC-2: Output filename mirrors input filename with .txt extension
        out = write_transcript("content", tmp_mp3_file, str(tmp_path / "out"))
        assert Path(out).name == "sample.txt"

    def test_written_file_contains_correct_content(self, tmp_path, tmp_mp3_file):
        # AC-1: Written file contains the formatted content exactly
        content = "Test transcript content"
        out = write_transcript(content, tmp_mp3_file, str(tmp_path / "out"))
        assert Path(out).read_text(encoding="utf-8") == content

    def test_creates_nested_output_directory(self, tmp_path, tmp_mp3_file):
        # AC-3: Create output directory (and parents) if missing
        nested = str(tmp_path / "a" / "b" / "c")
        out = write_transcript("content", tmp_mp3_file, nested)
        assert Path(out).exists()

    def test_returns_output_path_as_string(self, tmp_path, tmp_mp3_file):
        # AC-4: Return path to written file as a string
        out = write_transcript("content", tmp_mp3_file, str(tmp_path))
        assert isinstance(out, str)
        assert out.endswith(".txt")
