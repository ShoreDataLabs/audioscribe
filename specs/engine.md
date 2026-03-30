# Engine — Acceptance Criteria

## AC-1: Return segments with start, end, and text keys
Given an audio file path
When transcribe() is called
Then return a dict with "segments" list where each item has "start", "end", "text"

## AC-2: Return detected language
When transcribe() is called
Then return a dict with "language" key containing the detected language code

## AC-3: Load model only once across multiple transcribe calls
Given a TranscriptionEngine instance
When transcribe() is called multiple times
Then the underlying model is loaded exactly once (lazy + cached)

## AC-4: Pass language option to model when specified
Given language="fr" is passed to transcribe()
When transcribe() is called
Then model.transcribe is called with language="fr"

## AC-5: Return duration from last segment end time
When transcribe() returns a result with segments
Then result["duration"] equals the end time of the last segment

## AC-6: Return duration of 0.0 when there are no segments
When the model returns an empty segments list
Then result["duration"] == 0.0
