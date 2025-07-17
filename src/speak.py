from google.cloud import texttospeech
import os
import uuid
from playsound import playsound


def speak(text):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-F",  # or en-US-Wavenet-D for male
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    filename = f"temp_{uuid.uuid4()}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    playsound(filename)
    os.remove(filename)
