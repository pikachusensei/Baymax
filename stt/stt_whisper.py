import os

# Force ffmpeg path
os.environ["PATH"] += os.pathsep + r"C:\Users\Shreyansh Singh\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin"

import numpy as np
import sounddevice as sd
import whisper
import scipy.io.wavfile as wav


def record_audio(filename="temp.wave", duration=5, fs=16000):
    """Recored audio and save in wav"""

    print("Recording started")
    audio=sd.rec(int(duration*fs),samplerate=fs,channels=1,dtype=np.int16)
    sd.wait()
    wav.write(filename,fs,audio)
    print("Recording saved")
    return filename


def transcribe_audio():
    audio_file=record_audio()
    print("Transcribing audio")
    model=whisper.load_model("medium")
    result=model.transcribe(audio_file)
    text=result["text"]
    print("You said: ",text)
    return result["text"]   
