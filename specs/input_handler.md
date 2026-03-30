# Input Handler — Acceptance Criteria

## AC-1: Resolve single file to a one-item list
Given a path to a single audio file
When resolve_inputs() is called
Then return a list containing that file's path

## AC-2: Resolve directory to all audio files within it
Given a directory path containing audio files (and possibly non-audio files)
When resolve_inputs() is called
Then return a list of only audio file paths

## AC-3: Return empty list for directory with no audio files
Given a directory containing no audio files
When resolve_inputs() is called
Then return an empty list

## AC-4: Raise for nonexistent paths
Given a path that does not exist
When resolve_inputs() is called
Then raise FileNotFoundError

## AC-5: Results from directories are sorted alphabetically
Given a directory with multiple audio files
When resolve_inputs() is called
Then return files in sorted order for deterministic processing
