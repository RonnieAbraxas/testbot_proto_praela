"""
brain.py

Core reply-generation logic for TestBot.

Right now this uses a local Ollama server and the `gemma2b-instruct` model.
Later, we can:
- add error handling
- factor out prompt-building
- tweak temperature / top_p via config
"""

from typing import List, Tuple
import json
import urllib.request
import urllib.error


ConversationTurn = Tuple[str, str]  # (user, bot)
ConversationHistory = List[ConversationTurn]

# ---- Ollama config ----

# Make sure Ollama is running: `ollama serve`
# And that this model exists:  `ollama list`
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "gemma2:2b"


def _ollama_post(path: str, payload: dict) -> str:
    """
    Call the Ollama HTTP API at the given path with a JSON payload.
    We expect a streaming JSONL response and we concatenate the 'response' chunks.
    """
    url = f"{OLLAMA_BASE_URL}{path}"  # e.g. http://localhost:11434/api/generate
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    chunks: List[str] = []

    try:
        with urllib.request.urlopen(req) as resp:
            for line in resp:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                # If Ollama reports an error inside the JSON stream
                if "error" in obj:
                    raise RuntimeError(f"Ollama error: {obj['error']}")
                # Normal streamed text chunk
                if "response" in obj:
                    chunks.append(obj["response"])
    except urllib.error.HTTPError as e:
        # For now, just re-raise with more context; later we can handle gracefully
        raise RuntimeError(f"Ollama HTTP error {e.code}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Could not reach Ollama at {url}: {e.reason}") from e

    return "".join(chunks)


def _format_history(history: ConversationHistory) -> str:
    """
    Turn the conversation history into a simple text transcript.
    """
    lines: List[str] = []
    for user, bot in history:
        lines.append(f"User: {user}")
        lines.append(f"Bot:  {bot}")
    return "\n".join(lines)


def generate_reply(user_message: str, history: ConversationHistory) -> str:
    """
    Main brain entry point.

    - Takes the latest user message + prior history.
    - Builds a prompt.
    - Calls Ollama's /api/generate.
    - Returns the model's reply text.
    """
    history_text = _format_history(history)

    # Build a simple prompt that includes the transcript for context
    if history_text:
        prompt = (
            "You are a friendly, thoughtful chatbot.\n"
            "Here is the recent conversation between User and Bot:\n"
            f"{history_text}\n\n"
            "Now the user says:\n"
            f"{user_message}\n\n"
            "Reply as the Bot."
        )
    else:
        prompt = (
            "You are a friendly, thoughtful chatbot.\n"
            "The user says:\n"
            f"{user_message}\n\n"
            "Reply as the Bot."
        )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,  # we stream and reassemble chunks in _ollama_post
        # Later we might add:
        # "options": {
        #     "temperature": 0.7,
        #     "top_p": 0.9,
        # }
    }

    reply_text = _ollama_post("/api/generate", payload)
    return reply_text.strip()