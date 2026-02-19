# import sounddevice as sd
# from scipy.io.wavfile import write
# import whisper
# import os

# # -----------------------------
# # Configuration
# # -----------------------------
# SAMPLE_RATE = 16000
# DURATION = 7  # seconds
# RECORDINGS_DIR = "recordings"
# AUDIO_FILE_PATH = os.path.join(RECORDINGS_DIR, "input.wav")

# # -----------------------------
# # Create recordings folder if not exists
# # -----------------------------
# os.makedirs(RECORDINGS_DIR, exist_ok=True)

# print("Loading Whisper model...")
# model = whisper.load_model("base")
# #model = WhisperModel("models/faster-whisper-base")


# # -----------------------------
# # Record Audio
# # -----------------------------
# print(f"Recording for {DURATION} seconds... Speak now!")

# audio_data = sd.rec(
#     int(DURATION * SAMPLE_RATE),
#     samplerate=SAMPLE_RATE,
#     channels=1,
#     dtype="int16"
# )

# sd.wait()
# print("Recording finished.")

# # -----------------------------
# # Save to custom location
# # -----------------------------
# write(AUDIO_FILE_PATH, SAMPLE_RATE, audio_data)

# print(f"Audio saved at: {AUDIO_FILE_PATH}")

# # -----------------------------
# # Transcribe
# # -----------------------------
# print("Transcribing...")

# segments, _ = model.transcribe(AUDIO_FILE_PATH)

# transcribed_text = ""
# for segment in segments:
#     transcribed_text += segment.text

# print("\n📝 Transcribed Text:")
# print(transcribed_text.strip())



import sounddevice as sd
import whisper
import numpy as np

SAMPLE_RATE = 16000
DURATION = 5

print("Loading Whisper model...")
model = whisper.load_model("base")

print(f"Recording for {DURATION} seconds... Speak now!")

audio_data = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)

sd.wait()
print("Recording finished.")

print("Transcribing...")

audio_float32 = audio_data.flatten().astype(np.float32) / 32768.0

result = model.transcribe(audio_float32)

print("\n📝 Transcribed Text:")
print(result["text"].strip())
