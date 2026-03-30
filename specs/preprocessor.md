# Preprocessor — Acceptance Criteria

## AC-1: Convert non-WAV audio to WAV using from_file
Given a non-WAV audio file path
When preprocess() is called
Then AudioSegment.from_file is used to load it

## AC-2: Normalize WAV files using from_wav
Given a .wav file path
When preprocess() is called
Then AudioSegment.from_wav is used to load it

## AC-3: Convert audio to 16kHz sample rate
When preprocess() is called
Then set_frame_rate(16000) is called on the audio segment

## AC-4: Convert audio to mono (1 channel)
When preprocess() is called
Then set_channels(1) is called on the audio segment

## AC-5: Return path to a new temporary .wav file
When preprocess() is called
Then return a string path ending in ".wav"
