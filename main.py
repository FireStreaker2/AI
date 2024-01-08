import os
import time
import requests
from characterai import PyCAI
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

load_dotenv()

config = {
    "caiToken": os.getenv("CAI_TOKEN"),
    "caiCharacter": os.getenv("CAI_CHARACTER"),
    "ttsCharacter": os.getenv("TTS_CHARACTER"),
    "ttsAPIKey": os.getenv("TTS_API_KEY"),
}

client = PyCAI(config["caiToken"])
chat = client.chat.get_chat(config["caiCharacter"])

participants = chat["participants"]
if not participants[0]["is_human"]:
    tgt = participants[0]["user"]["username"]
else:
    tgt = participants[1]["user"]["username"]

try:
    while True:
        message = input("You: ")

        data = client.chat.send_message(chat["external_id"], tgt, message)

        name = data["src_char"]["participant"]["name"]
        text = data["replies"][0]["text"]

        print(f"{name}: {text}")

        response = requests.post(
            "https://api.topmediai.com/v1/text2speech",
            json={
                "text": text,
                "speaker": config["ttsCharacter"],
                "emotion": "Neutral",
            },
            headers={
                "accept": "application/json",
                "x-api-key": config["ttsAPIKey"],
                "Content-Type": "application/json",
            },
        )

        if response.status_code == 200:
            data = response.json()
            url = requests.get(data["data"]["oss_url"])

            with open("out.wav", "wb") as file:
                file.write(url.content)

            audio = AudioSegment.from_file("out.wav", format="mp3")
            play(audio)

        else:
            print("Error generating TTS")


except KeyboardInterrupt:
    os.remove("out.wav")
