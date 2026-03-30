import pytest
from pathlib import Path
from src.validator import validate


class TestValidate:
    @pytest.mark.parametrize("ext", [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac", ".wma"])
    def test_accepts_supported_formats(self, tmp_path, ext):
        # AC-1: Accept supported audio formats
        f = tmp_path / f"audio{ext}"
        f.write_bytes(b"\x00" * 10)
        assert validate(str(f)) is True

    def test_rejects_unsupported_format(self, tmp_path):
        # AC-2: Reject unsupported file formats
        f = tmp_path / "document.pdf"
        f.write_bytes(b"\x00" * 10)
        with pytest.raises(ValueError, match="Unsupported format"):
            validate(str(f))

    def test_rejects_nonexistent_file(self, tmp_path):
        # AC-3: Reject files that do not exist
        with pytest.raises(FileNotFoundError):
            validate(str(tmp_path / "ghost.mp3"))

    def test_rejects_file_over_size_limit(self, tmp_path, monkeypatch):
        # AC-4: Reject files exceeding 500MB
        f = tmp_path / "huge.mp3"
        f.write_bytes(b"\x00" * 10)

        class _FakeStat:
            st_size = 600 * 1024 * 1024  # 600MB

        monkeypatch.setattr(Path, "stat", lambda self, **kwargs: _FakeStat())
        with pytest.raises(ValueError, match="File too large"):
            validate(str(f))

    def test_accepts_directory_in_batch_mode(self, tmp_path):
        # AC-5: Accept directory paths when batch=True
        assert validate(str(tmp_path), batch=True) is True

    def test_rejects_file_path_in_batch_mode(self, tmp_wav_file):
        # AC-6: Reject non-directory paths in batch mode
        with pytest.raises(NotADirectoryError):
            validate(tmp_wav_file, batch=True)
