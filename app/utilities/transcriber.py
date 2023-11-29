import openai
from fastapi import UploadFile

class Transcriber:
    def __init__(self):
        pass
        
    def transcribe(self, audio: UploadFile):
        with open("audio.mp3", "wb") as audio_file:
            audio_file.write(audio.file.read())

        audio_file= open("audio.mp3", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript.text