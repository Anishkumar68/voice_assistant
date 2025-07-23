import asyncio
import edge_tts
import os
import uuid
from playsound import playsound


async def speak_async(text, voice="en-US-JennyNeural"):
    if not os.path.exists("audio"):
        os.makedirs("audio")

    filename = f"temp_{uuid.uuid4()}.mp3"
    filepath = os.path.join("audio", filename)

    try:
        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(filepath)

        if os.path.exists(filepath):
            playsound(filepath)
        else:
            print(f"❌ File not created: {filepath}")

    except Exception as e:
        print(f"❌ TTS error: {e}")

    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"⚠️ Failed to delete temp file: {e}")


def speak(text, voice="en-US-JennyNeural"):
    asyncio.run(speak_async(text, voice=voice))
