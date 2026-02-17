import tempfile
from faster_whisper import WhisperModel

class SpeechService:

    def __init__(self):
        self.model = WhisperModel("base", compute_type="float32")

    def transcribe(self, audio_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name

        segments, _ = self.model.transcribe(tmp_path)

        text = ""
        for segment in segments:
            text += segment.text

        return text.strip()

    def check_wake_word(self, text, wake_word="jarvis"):
        text_lower = text.lower()

        if text_lower.startswith(wake_word):
            cleaned = text_lower.replace(wake_word, "", 1).strip()
            return True, cleaned

        return False, None
