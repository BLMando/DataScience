# RASA GameGuru

## Setup
To setup the environment, follow these instructions once you `cd`'d into `Progetto_Chatbot`:

```bash
uv venv --python 3.8 .
source .venv/bin/activate # macOS/Linux
.\.venv\Scripts\Activate.ps1 # windows
uv pip install rasa aiogram 
```

## Running (you need to activate venv)
You'll need two/three shells
- run actions (this is what actually handles execution)
    ```bash
    rasa run actions
    ```
- run rasa model (this is where NLP happens)
    ```bash
    rasa run --enable-api --cors "*" --debug
    ```
- (optional) use `rasa shell` to interect with bot
- (optional) use telegram bot to interect with bot
