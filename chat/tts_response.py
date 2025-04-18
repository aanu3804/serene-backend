import os
import uuid
import logging
import pyttsx3

from gtts import gTTS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

output_dir = "static/audio"
os.makedirs(output_dir, exist_ok=True)

# Try to initialize pyttsx3
try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
    logger.info("pyttsx3 initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize pyttsx3: {e}")
    engine = None

def generate_tts(text):
    if not text:
        logger.warning("No text provided for TTS")
        return None

    filename = f"serene_{uuid.uuid4().hex}.mp3"
    path = os.path.join(output_dir, filename)

    # Use pyttsx3 if available
    if engine:
        try:
            logger.info(f"Generating TTS using pyttsx3: {path}")
            engine.save_to_file(text, path)
            engine.runAndWait()
            if os.path.exists(path):
                return path
            else:
                logger.warning("pyttsx3 failed to create the audio file. Falling back to gTTS.")
        except Exception as e:
            logger.error(f"pyttsx3 TTS generation failed: {e}")

    # Fallback to gTTS
    try:
        logger.info(f"Generating TTS using gTTS: {path}")
        tts = gTTS(text=text, lang='en')
        tts.save(path)
        return path
    except Exception as e:
        logger.error(f"gTTS generation failed: {e}")
        return None
