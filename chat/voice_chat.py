from pydub import AudioSegment
import os
import speech_recognition as sr

def transcribe_audio(file_path):
    # Convert .webm to .wav if needed
    if file_path.endswith(".webm"):
        wav_path = file_path.replace(".webm", ".wav")
        audio = AudioSegment.from_file(file_path)
        audio.export(wav_path, format="wav")
        file_path = wav_path

    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
        try:
            transcript = r.recognize_google(audio_data)
            return transcript
        except sr.UnknownValueError:
            return "I couldn’t quite catch that—could you try again?"
        except sr.RequestError:
            return "I’m having trouble connecting to the speech API—let’s try typing instead!"