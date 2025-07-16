import os
import wave
import json
import pyaudio
import pyttsx3
from vosk import Model, KaldiRecognizer
import asyncio
import edge_tts


# from playsound import playsound
import uuid

# Set model path
VOSK_MODEL_PATH = os.path.join("Models", "vosk-model-small-en-us-0.15")
AUDIO_DIR = os.path.join("RAG", "audio")
AUDIO_FILE = os.path.join(AUDIO_DIR, "audio_input.wav")

# Load VOSK model
model = Model(VOSK_MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)


def record_audio_to_file(file_path, record_seconds=5):
    """Records voice input from mic and saves as a .wav file."""
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    print("🎙️ Recording... Speak now.")
    frames = []

    for _ in range(0, int(16000 / 1024 * record_seconds)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(file_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))


def listen_from_file(file_path):
    """Transcribes speech from a saved .wav file using VOSK."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    results = []
    wf = wave.open(file_path, "rb")

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            results.append(result.get("text", ""))

    final = json.loads(recognizer.FinalResult())
    results.append(final.get("text", ""))

    return " ".join(results).strip()


def speak(text):
    """Speaks a text string using espeak."""
    os.system(f'espeak "{text}"')


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# def speak(text):
#     asyncio.run(speak_async(text))


# async def speak_async(text):
#     filename = f"temp_{uuid.uuid4()}.mp3"
#     communicate = edge_tts.Communicate(text=text, voice="en-US-JennyNeural")
#     await communicate.save(filename)
#     os.system(filename)


# async def speak_async(text):
#     filename = f"temp_{uuid.uuid4()}.mp3"
#     communicate = edge_tts.Communicate(text=text, voice="en-US-JennyNeural")
#     await communicate.save(filename)
#     playsound(filename)
#     os.remove(filename)


# def speak(text):
#     asyncio.run(speak_async(text))


def listen():
    """Main interface: records if file doesn't exist, then transcribes."""
    record_audio_to_file(AUDIO_FILE)
    return listen_from_file(AUDIO_FILE)
