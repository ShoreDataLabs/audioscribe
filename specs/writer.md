# Writer — Acceptance Criteria

## AC-1: Write transcript content to a .txt file in the output directory
Given formatted transcript content, an input audio path, and an output directory
When write_transcript() is called
Then a .txt file is created in the output directory containing that content

## AC-2: Output filename mirrors input filename with .txt extension
Given an input path of "interview.mp3"
When write_transcript() is called
Then the output file is named "interview.txt"

## AC-3: Create output directory if it does not exist
Given an output directory path that does not yet exist
When write_transcript() is called
Then the directory (and any parents) is created before writing

## AC-4: Return the output file path as a string
When write_transcript() is called
Then return the absolute path to the written file as a string
