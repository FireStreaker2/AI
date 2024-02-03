import os
import time
import requests
import g4f
from characterai import PyCAI
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

config = {
    "caiToken": os.getenv("CAI_TOKEN"),
    "caiCharacter": os.getenv("CAI_CHARACTER"),
    "openAIToken": os.getenv("OPENAI_TOKEN"),
    "openAIModel": "gpt-3.5-turbo",
    "g4fModel": "gpt-3.5-turbo",
    "g4fProvider": g4f.Provider.Vercel,
    "huggingfaceModel": os.getenv("HUGGINGFACE_MODEL"),
    "huggingfaceToken": os.getenv("HUGGINGFACE_TOKEN"),
    "aiMethod": "CAI",
}

if config["aiMethod"] == "CAI":
    client = PyCAI(config["caiToken"])
    chat = client.chat.get_chat(config["caiCharacter"])

    participants = chat["participants"]
    if not participants[0]["is_human"]:
        tgt = participants[0]["user"]["username"]
        bot = participants[0]["name"]

    else:
        tgt = participants[1]["user"]["username"]
        bot = participants[1]["name"]

elif config["aiMethod"] == "G4F":
    history = []

    bot = config["g4fModel"]

elif config["aiMethod"] == "HUGGING":
    history = {
        "user": [],
        "ai": [],
    }

    bot = config["huggingfaceModel"].split("/")[-1]

else:
    client = OpenAI(api_key=config["openAIToken"])
    history = []

    bot = config["openAIModel"]

print(f"Now chatting with: {bot}")

try:
    while True:
        message = input("You: ")

        if config["aiMethod"] == "CAI":
            data = client.chat.send_message(chat["external_id"], tgt, message)

            name = data["src_char"]["participant"]["name"]
            text = data["replies"][0]["text"]

        elif config["aiMethod"] == "G4F":
            history.append({"role": "user", "content": message})

            name = config["g4fModel"]
            text = g4f.ChatCompletion.create(
                model=config["g4fModel"],
                messages=history,
            )

            history.append({"role": "assistant", "content": text})

        elif config["aiMethod"] == "HUGGING":
            name = config["huggingfaceModel"].split("/")[-1]

            response = requests.post(
                config["huggingfaceModel"],
                headers={"Authorization": f"Bearer {config['huggingfaceToken']}"},
                json={
                    "inputs": {
                        "past_user_inputs": history["user"],
                        "generated_responses": history["ai"],
                        "text": message,
                    },
                },
            )

            data = response.json()
            text = data["generated_text"]

            history["user"].append(message)
            history["ai"].append(text)

        else:
            history.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=config["openAIModel"],
                messages=history,
            )

            name = config["openAIModel"]
            text = response["choices"][0]["message"]["content"]

            history.append({"role": "assistant", "content": text})

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
