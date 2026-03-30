class TranscriptionEngine:
    def __init__(self, model_size: str = "medium"):
        self.model_size = model_size
        self._model = None

    def _load_model(self):
        if self._model is None:
            import whisper
            self._model = whisper.load_model(self.model_size)
        return self._model

    def transcribe(self, audio_path: str, language: str = None) -> dict:
        model = self._load_model()

        kwargs = {}
        if language:
            kwargs["language"] = language

        result = model.transcribe(audio_path, **kwargs)

        segments = [
            {
                "start": s["start"],
                "end": s["end"],
                "text": s["text"].strip(),
            }
            for s in result["segments"]
        ]

        return {
            "text": result["text"].strip(),
            "segments": segments,
            "language": result["language"],
            "duration": segments[-1]["end"] if segments else 0.0,
        }
