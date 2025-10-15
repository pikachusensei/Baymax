# import pyttsx3
from gtts import gTTS
import os
import playsound

def speak_hi(text,filename="baymax_hi.mp3"):
    print("🤖 Baymax: ",text)
    tts=gTTS(text=text,lang="hi")
    tts.save(filename)
    # os.system(f"mpg321 {filename}")
    playsound.playsound(filename)
    os.remove(filename)