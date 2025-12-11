"""
cli.py

Command-line interface for TestBot.

Responsibilities:
- manage the conversation loop
- collect user input
- call the brain to generate replies
- maintain in-memory history
- persist the conversation to a phase-specific log file as messages are exchanged
"""

from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from app.brain import generate_reply


ConversationTurn = Tuple[str, str]  # (user, bot)
ConversationHistory = List[ConversationTurn]

# Helper Tools: These functions assist the new real-time logging and timestamping functions

def timestamp() -> str:
    """Return an ISO-like timestamp for log lines."""
    return datetime.now().isoformat(timespec="seconds")


def get_log_dir(phase: str) -> Path:
    """
    Ensure the log directory for this phase exists and return its Path.
    Example: logs/echobot
    """
    base = Path("logs") / phase
    base.mkdir(parents=True, exist_ok=True)
    return base


def make_log_file_path(phase: str) -> Path:
    """
    Build a new log file path with a timestamped filename.
    Example: logs/echobot/2025-12-09_11-45-30__echobot.txt
    """
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return get_log_dir(phase) / f"{ts}__{phase}.txt"

# Input Handling for pasted multiline messages

def read_user_message() -> str:
    """
    Read a user message from stdin.

    Normal mode:
      - User types a single line and presses Enter.

    Paste mode:
      - User types /paste and presses Enter.
      - Then pastes multiple lines.
      - Ends with a line containing only /end.
      - All pasted lines are joined into one message.
    """
    first = input("You: ")

    if first.strip() == "/paste":
        print("Paste your message. When you're done, type /end on its own line.")
        lines: list[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                break  # end of input
            if line.strip() == "/end":
                break
            lines.append(line)
        # Join with newlines so the poem / prompt keeps its structure
        return "\n".join(lines).strip()

    return first


# Conversation & Logging Loop

def run_cli() -> None:
    phase = "1_echobot"
    print(f"Starting TestBot... (phase: {phase}; type 'quit' or 'exit' to end)")

    # Conversation history still kept for the brain
    history: ConversationHistory = []

    # 1. Create a fresh log file path for this conversation
    log_path = make_log_file_path(phase)

    # 2. Open the log file once and keep it open during the whole conversation
    with log_path.open("a", encoding="utf-8") as log_file:
        # 2a. Write a header for this conversation
        started_at = timestamp()
        log_file.write("=== New Conversation ===\n")
        log_file.write(f"phase: {phase}\n")
        log_file.write(f"started: {started_at}\n\n")
        log_file.flush()

        # 3. Main conversation loop
        while True:
            user = read_user_message()

            # Log user message with aesthetic spacing
            log_file.write(f"{timestamp()}\n")
            log_file.write(f"User: {user}\n\n")
            log_file.flush()

            # Log final user message 
            if user.lower() in ("quit", "exit"):
                log_file.write(f"{timestamp()}\n")
                log_file.write(f"User: {user}")
                log_file.flush()

                reply = "Goodbye!"
                print(f"Bot: {reply}")
            
                # Log final bot reply with matching formatting
                log_file.write(f"{timestamp()}\n")
                log_file.write(f"Bot:  {reply}\n\n")
                log_file.flush()

                # Update in-memory history
                history.append((user, reply))
                break

            # Ask the brain for a reply, passing current history
            reply = generate_reply(user, history)
            print("Bot:", reply)

            # Log the bot reply with aesthetic spacing
            log_file.write(f"{timestamp()}\n")
            log_file.write(f"Bot:  {reply}\n\n")
            log_file.flush()

             # Update in-memory history
            history.append((user, reply))