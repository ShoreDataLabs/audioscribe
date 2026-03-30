import sys
import pytest
from unittest.mock import MagicMock, patch
from src.engine import TranscriptionEngine


def _make_mock_whisper(whisper_result):
    mock_model = MagicMock()
    mock_model.transcribe.return_value = whisper_result
    mock_whisper = MagicMock()
    mock_whisper.load_model.return_value = mock_model
    return mock_whisper, mock_model


class TestTranscriptionEngine:
    def test_model_loaded_only_once_across_multiple_calls(self, tmp_wav_file, whisper_result):
        # AC-3: Load model once and cache it
        engine = TranscriptionEngine(model_size="base")
        mock_whisper, _ = _make_mock_whisper(whisper_result)

        with patch.dict(sys.modules, {"whisper": mock_whisper}):
            engine.transcribe(tmp_wav_file)
            engine.transcribe(tmp_wav_file)

        mock_whisper.load_model.assert_called_once_with("base")

    def test_returns_segments_with_required_keys(self, tmp_wav_file, whisper_result):
        # AC-1: Return segments with start, end, text keys
        engine = TranscriptionEngine()
        mock_whisper, _ = _make_mock_whisper(whisper_result)

        with patch.dict(sys.modules, {"whisper": mock_whisper}):
            result = engine.transcribe(tmp_wav_file)

        assert "segments" in result
        for seg in result["segments"]:
            assert "start" in seg
            assert "end" in seg
            assert "text" in seg

    def test_returns_detected_language(self, tmp_wav_file, whisper_result):
        # AC-2: Return detected language in result
        engine = TranscriptionEngine()
        mock_whisper, _ = _make_mock_whisper(whisper_result)

        with patch.dict(sys.modules, {"whisper": mock_whisper}):
            result = engine.transcribe(tmp_wav_file)

        assert result["language"] == "en"

    def test_passes_language_to_model_when_specified(self, tmp_wav_file, whisper_result):
        # AC-4: Pass language option to model.transcribe when specified
        engine = TranscriptionEngine()
        mock_whisper, mock_model = _make_mock_whisper(whisper_result)

        with patch.dict(sys.modules, {"whisper": mock_whisper}):
            engine.transcribe(tmp_wav_file, language="fr")

        mock_model.transcribe.assert_called_with(tmp_wav_file, language="fr")

    def test_no_language_kwarg_when_not_specified(self, tmp_wav_file, whisper_result):
        # AC-4 inverse: Don't pass language if not specified
        engine = TranscriptionEngine()
        mock_whisper, mock_model = _make_mock_whisper(whisper_result)

        with patch.dict(sys.modules, {"whisper": mock_whisper}):
            engine.transcribe(tmp_wav_file)

        mock_model.transcribe.assert_called_with(tmp_wav_file)

    def test_duration_equals_last_segment_end(self, tmp_wav_file, whisper_result):
        # AC-5: Duration is the end time of the last segment
        engine = TranscriptionEngine()
        mock_whisper, _ = _make_mock_whisper(whisper_result)

        with patch.dict(sys.modules, {"whisper": mock_whisper}):
            result = engine.transcribe(tmp_wav_file)

        assert result["duration"] == whisper_result["segments"][-1]["end"]

    def test_duration_is_zero_when_no_segments(self, tmp_wav_file):
        # AC-6: Duration is 0.0 when segments list is empty
        engine = TranscriptionEngine()
        empty_result = {"text": "", "segments": [], "language": "en"}
        mock_whisper, _ = _make_mock_whisper(empty_result)

        with patch.dict(sys.modules, {"whisper": mock_whisper}):
            result = engine.transcribe(tmp_wav_file)

        assert result["duration"] == 0.0
        assert result["segments"] == []
