# app/brain.py

from typing import List, Tuple
import json

ConversationTurn = Tuple[str, str]
ConversationHistory = List[ConversationTurn]

# --- Ollama config (used later) ---
OLLAMA_BASE_URL = "http://localhost:11434"
BASE_MODEL = "gemma2:2b"

def _ollama_post(path: str, payload: dict) -> str:
    """
    Call the Ollama HTTP API and return the generated text.
   """
    url = f'{OLLAMA_BASE_URL}/{path.lstrip('/')}'
    print('DEBUG: _ollama_post was called')
    data = json.dumps(payload).encode('UTF-8')
    return ""


def generate_reply(user_msg: str, history: ConversationHistory) -> str:
    payload = {
        "model": BASE_MODEL,
        "prompt": user_msg,
        "stream": False,
    }
    _ollama_post("api/generate", payload)
    return f"(stub) I received: {user_msg}"

