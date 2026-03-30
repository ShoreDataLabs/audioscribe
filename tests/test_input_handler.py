import pytest
from pathlib import Path
from src.input_handler import resolve_inputs


class TestResolveInputs:
    def test_single_file_returns_one_item_list(self, tmp_wav_file):
        # AC-1: Resolve single file path to list
        result = resolve_inputs(tmp_wav_file)
        assert result == [tmp_wav_file]

    def test_directory_returns_only_audio_files(self, tmp_path):
        # AC-2: Resolve directory to list of audio files, excluding non-audio
        (tmp_path / "a.mp3").write_bytes(b"\x00" * 10)
        (tmp_path / "b.wav").write_bytes(b"\x00" * 10)
        (tmp_path / "notes.txt").write_bytes(b"\x00" * 10)
        (tmp_path / "image.png").write_bytes(b"\x00" * 10)

        result = resolve_inputs(str(tmp_path))
        names = [Path(f).name for f in result]

        assert "a.mp3" in names
        assert "b.wav" in names
        assert "notes.txt" not in names
        assert "image.png" not in names

    def test_empty_directory_returns_empty_list(self, tmp_path):
        # AC-3: Return empty list for directory with no audio files
        (tmp_path / "readme.txt").write_bytes(b"\x00" * 10)
        assert resolve_inputs(str(tmp_path)) == []

    def test_raises_for_nonexistent_path(self, tmp_path):
        # AC-4: Raise FileNotFoundError for paths that don't exist
        with pytest.raises(FileNotFoundError):
            resolve_inputs(str(tmp_path / "ghost"))

    def test_directory_results_are_sorted(self, tmp_path):
        # AC-5: Results are sorted alphabetically for deterministic ordering
        (tmp_path / "c.mp3").write_bytes(b"\x00" * 10)
        (tmp_path / "a.wav").write_bytes(b"\x00" * 10)
        (tmp_path / "b.flac").write_bytes(b"\x00" * 10)

        result = resolve_inputs(str(tmp_path))
        names = [Path(f).name for f in result]
        assert names == sorted(names)
