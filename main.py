import os
import time
import requests
from characterai import PyCAI
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

config = {
    "caiToken": os.getenv("CAI_TOKEN"),
    "caiCharacter": os.getenv("CAI_CHARACTER"),
}

client = PyCAI(config["caiToken"])
chat = client.chat.get_chat(config["caiCharacter"])

participants = chat["participants"]
if not participants[0]["is_human"]:
    tgt = participants[0]["user"]["username"]
    bot = participants[0]["name"]

else:
    tgt = participants[1]["user"]["username"]
    bot = participants[1]["name"]

print(f"Now chatting with: {bot}")

try:
    while True:
        message = input("You: ")

        data = client.chat.send_message(chat["external_id"], tgt, message)

        name = data["src_char"]["participant"]["name"]
        text = data["replies"][0]["text"]

        print(f"{name}: {text}")

        tts = gTTS(text, lang="en")
        tts.save("out.mp3")

        audio = AudioSegment.from_file("out.mp3", format="mp3")
        play(audio)


except KeyboardInterrupt:
    try:
        os.remove("out.mp3")
    except Exception:
        pass
