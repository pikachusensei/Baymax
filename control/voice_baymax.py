import pvporcupine
import pyaudio
import struct
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from dotenv import load_dotenv
import os, sys
import subprocess

load_dotenv()
if getattr(sys, 'frozen', False):
    dir_path = os.path.dirname(sys.executable)
else:
    dir_path = os.path.dirname(os.path.abspath(__file__))

# hide terminal window on Windows
if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


# Load your fine-tuned model
MODEL_PATH = "C:/Users/Shreyansh Singh/Desktop/Baymax/baymax/control/baymax_finetuned"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, local_files_only=True)

# Initialize speech recognizer
recognizer = sr.Recognizer()


porcupine = pvporcupine.create(
    access_key=os.getenv("ACCESS_KEY"),
    keyword_paths=["C:/Users/Shreyansh Singh/Desktop/Baymax/baymax/control/wake_word/Jarvis_en_windows_v3_0_0.ppn"]
) # later replace with “hey baymax”


pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=porcupine.sample_rate,
                 input=True,
                 frames_per_buffer=porcupine.frame_length)

def listen():
    """Listen for user's voice input"""
    with sr.Microphone() as source:
        print("🎧 Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You:", text)
            return text
        except sr.UnknownValueError:
            print("❌ Didn't catch that.")
            return None

def speak(text):
    """Speak using gTTS"""
    tts = gTTS(text=text, lang='en')
    tts.save("baymax_reply.mp3")
    playsound("baymax_reply.mp3")
    os.remove("baymax_reply.mp3")

def get_baymax_reply(user_input):
    """Generate a reply from Baymax"""
    inputs = tokenizer(f"User: {user_input}\nBaymax:", return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    reply = reply.split("Baymax:")[-1].strip()
    print("Baymax:", reply)
    return reply

print("🩺 Baymax is online! Say 'Hey Baymax' to wake me up.")

while True:
    pcm = stream.read(porcupine.frame_length)
    pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

    keyword_index = porcupine.process(pcm_unpacked)
    if keyword_index >= 0:
        print("🩺 Baymax activated! Listening for your question...")
        user_input = listen()
        if user_input:
            reply = get_baymax_reply(user_input)
            speak(reply)
