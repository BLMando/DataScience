# RASA GameGuru

## Setup

To setup the environment, follow these instructions once you `cd`'d into `Progetto_Chatbot`:

```bash
uv venv --python 3.8 .
source .venv/bin/activate # macOS/Linux
.\.venv\Scripts\activate.ps1 # windows
uv pip uninstall -y psycopg2-binary
uv pip install psycopg2-binary==2.9.9 rasa aiogram 
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
