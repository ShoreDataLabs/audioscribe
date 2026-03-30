# Validator — Acceptance Criteria

## AC-1: Accept supported audio formats
Given a path to a file with extension in [.mp3, .wav, .m4a, .ogg, .flac, .aac, .wma]
When validate() is called
Then return True with no errors

## AC-2: Reject unsupported file formats
Given a path to a file with an extension not in the supported list
When validate() is called
Then raise ValueError with message containing "Unsupported format"

## AC-3: Reject files that do not exist
Given a path to a file that does not exist on disk
When validate() is called
Then raise FileNotFoundError

## AC-4: Reject files exceeding the size limit (500MB)
Given a path to a file larger than 500MB
When validate() is called
Then raise ValueError with message containing "File too large"

## AC-5: Accept directory paths in batch mode
Given a directory path and batch=True
When validate() is called
Then return True

## AC-6: Reject non-directory paths in batch mode
Given a file path and batch=True
When validate() is called
Then raise NotADirectoryError
