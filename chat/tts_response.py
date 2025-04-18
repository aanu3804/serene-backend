import pyttsx3
import uuid
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

output_dir = "static/audio"
os.makedirs(output_dir, exist_ok=True)

try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)
except Exception as e:
    logger.error(f"Failed to initialize pyttsx3: {e}")
    engine = None

def generate_tts(text):
    if not engine:
        logger.error("TTS engine not initialized")
        return None
    if not text:
        logger.warning("No text provided for TTS")
        return None

    try:
        filename = f"serene_{uuid.uuid4().hex}.wav"
        path = os.path.join(output_dir, filename)
        logger.info(f"Generating TTS file: {path}")
        
        engine.save_to_file(text, path)
        engine.runAndWait()
        
        if not os.path.exists(path):
            logger.error(f"TTS file not created: {path}")
            return None
            
        logger.info(f"TTS file created successfully: {path}")
        return path
    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        return None