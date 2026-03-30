from unittest.mock import patch
from src.preprocessor import preprocess


class TestPreprocess:
    def test_calls_ffmpeg_for_non_wav(self, tmp_mp3_file):
        # AC-1: Use ffmpeg to convert non-WAV files
        with patch("src.preprocessor.subprocess.run") as mock_run:
            preprocess(tmp_mp3_file)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "ffmpeg"
        assert tmp_mp3_file in args

    def test_calls_ffmpeg_for_wav(self, tmp_wav_file):
        # AC-2: Use ffmpeg to normalize WAV files too
        with patch("src.preprocessor.subprocess.run") as mock_run:
            preprocess(tmp_wav_file)
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args[0] == "ffmpeg"

    def test_sets_sample_rate_to_16khz(self, tmp_mp3_file):
        # AC-3: Pass -ar 16000 flag to ffmpeg
        with patch("src.preprocessor.subprocess.run") as mock_run:
            preprocess(tmp_mp3_file)
        args = mock_run.call_args[0][0]
        assert "-ar" in args
        assert "16000" in args

    def test_sets_mono_channel(self, tmp_mp3_file):
        # AC-4: Pass -ac 1 flag to ffmpeg for mono output
        with patch("src.preprocessor.subprocess.run") as mock_run:
            preprocess(tmp_mp3_file)
        args = mock_run.call_args[0][0]
        assert "-ac" in args
        assert "1" in args

    def test_returns_wav_path_string(self, tmp_mp3_file):
        # AC-5: Return path to temporary .wav file as a string
        with patch("src.preprocessor.subprocess.run"):
            result = preprocess(tmp_mp3_file)
        assert isinstance(result, str)
        assert result.endswith(".wav")
