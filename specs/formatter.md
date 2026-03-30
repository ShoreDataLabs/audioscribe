# Formatter — Acceptance Criteria

## AC-1: Include metadata header in output
Given metadata (filename, date, duration, language, model)
When format_transcript() is called
Then output contains all metadata fields in a structured header

## AC-2: Format each segment with a [HH:MM:SS] timestamp prefix
Given segments with start times in seconds
When format_transcript() is called
Then each segment line begins with [HH:MM:SS]

## AC-3: Handle empty segments list gracefully
Given an empty segments list
When format_transcript() is called
Then return a valid transcript with header and footer but no segment lines

## AC-4: Include clear separators and END marker
When format_transcript() is called
Then output contains separator lines (===) and "END OF TRANSCRIPTION" footer

## AC-5: Wrap long lines so no line exceeds 70 characters
Given a segment with text longer than 59 characters
When format_transcript() is called
Then that segment's text is wrapped with continuation lines indented to align with text start
