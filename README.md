![AI](https://socialify.git.ci/FireStreaker2/AI/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pulls=1&stargazers=1&theme=Dark)

# About
AI is a simple program to talk to artificial intelligence. It supports many different ways of communication, and different types of LLMs.

# Features
- [x] Text to text
- [x] Text to speech
- [x] Speech to text
- [x] Speech to speech
- [x] Ability to customize source of AI

# Usage
## Setup
```bash
$ git clone https://github.com/FireStreaker2/AI.git
$ cd AI
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ cp .env.example .env
$ python main.py
```

## Configuration
In order to configure how this program works, you can edit your ``.env`` file to include the values you want. Alternatively, you can also manually modify the following ``config`` dictionary located in ``main.py``.
```python
config = {
    "caiToken": os.getenv("CAI_TOKEN"),
    "caiCharacter": os.getenv("CAI_CHARACTER"),
    "openAIToken": os.getenv("OPENAI_TOKEN"),
    "openAIModel": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
    "g4fModel": os.getenv("G4F_MODEL", "gpt-3.5-turbo"),
    "g4fProvider": os.getenv("G4F_PROVIDER", g4f.Provider.Vercel),
    "huggingfaceModel": os.getenv("HUGGINGFACE_MODEL"),
    "huggingfaceToken": os.getenv("HUGGINGFACE_TOKEN"),
    "inputMethod": "text",
    "outputMethod": "text",
    "aiMethod": os.getenv("AI_METHOD", "CAI"),
}
```

# License
[MIT](https://github.com/FireStreaker2/AI/blob/main/LICENSE)