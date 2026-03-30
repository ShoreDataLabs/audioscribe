import pytest
from src.formatter import format_transcript, _format_timestamp, _format_duration


class TestFormatTimestamp:
    def test_zero_seconds(self):
        assert _format_timestamp(0.0) == "[00:00:00]"

    def test_seconds_only(self):
        assert _format_timestamp(45.0) == "[00:00:45]"

    def test_minutes_and_seconds(self):
        assert _format_timestamp(90.0) == "[00:01:30]"

    def test_hours_minutes_seconds(self):
        assert _format_timestamp(3661.0) == "[01:01:01]"

    def test_fractional_seconds_are_truncated(self):
        assert _format_timestamp(5.9) == "[00:00:05]"


class TestFormatDuration:
    def test_zero(self):
        assert _format_duration(0.0) == "00:00"

    def test_under_one_hour(self):
        assert _format_duration(90.0) == "01:30"

    def test_over_one_hour(self):
        assert _format_duration(3661.0) == "01:01:01"


class TestFormatTranscript:
    def test_contains_all_metadata_fields(self, sample_metadata, sample_segments):
        # AC-1: Metadata header includes filename, date, language, model
        content = format_transcript(sample_metadata, sample_segments)
        assert "interview.mp3" in content
        assert "2026-03-30" in content
        assert "en" in content
        assert "medium" in content

    def test_segments_have_timestamp_prefix(self, sample_metadata, sample_segments):
        # AC-2: Each segment line starts with [HH:MM:SS]
        content = format_transcript(sample_metadata, sample_segments)
        assert "[00:00:00]" in content
        assert "[00:00:05]" in content
        assert "[00:00:12]" in content

    def test_empty_segments_produces_valid_output(self, sample_metadata):
        # AC-3: Handle empty segments gracefully
        content = format_transcript(sample_metadata, [])
        assert "TRANSCRIPTION" in content
        assert "END OF TRANSCRIPTION" in content

    def test_output_has_separators_and_footer(self, sample_metadata, sample_segments):
        # AC-4: Clear separators and END marker present
        content = format_transcript(sample_metadata, sample_segments)
        assert "=" * 40 in content
        assert "END OF TRANSCRIPTION" in content

    def test_no_line_exceeds_70_characters(self, sample_metadata, sample_segments):
        # AC-5: Long text is wrapped; no line exceeds 70 chars
        content = format_transcript(sample_metadata, sample_segments)
        for line in content.splitlines():
            assert len(line) <= 70, f"Line too long ({len(line)}): {line!r}"

    def test_continuation_lines_are_indented(self, sample_metadata):
        # AC-5: Continuation lines align with text start (11-space indent)
        long_segment = [
            {
                "start": 0.0,
                "end": 5.0,
                "text": (
                    "This sentence is intentionally long enough to require wrapping "
                    "onto a second line with proper indentation alignment."
                ),
            }
        ]
        content = format_transcript(sample_metadata, long_segment)
        lines = content.splitlines()
        ts_line_idx = next(i for i, l in enumerate(lines) if l.startswith("[00:00:00]"))
        continuation = lines[ts_line_idx + 1]
        assert continuation.startswith(" " * 11)
