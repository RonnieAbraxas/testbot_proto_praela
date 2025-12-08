"""
cli.py

Command-line interface for TestBot.

Responsibilities:
- manage the conversation loop
- collect user input
- call the brain to generate replies
- maintain in-memory history
- persist the conversation to a text file on exit
"""

from typing import List, Tuple
from pathlib import Path

from app.brain import generate_reply


ConversationTurn = Tuple[str, str]  # (user, bot)
ConversationHistory = List[ConversationTurn]


def run_cli() -> None:
    print("Starting TestBot... (type 'quit' or 'exit' to end)")
    history: ConversationHistory = []

    while True:
        user = input("You: ").strip()

        if user.lower() in ("quit", "exit"):
            reply = "Goodbye!"
            print(f"Bot: {reply}")

            # Record the final turn as well
            history.append((user, reply))

            # Persist history to a file
            write_history(history)
            break

        reply = generate_reply(user, history)
        print("Bot:", reply)

        # Save the turn
        history.append((user, reply))


def write_history(history: ConversationHistory, filename: str = "history2.txt") -> None:
    """
    Append the conversation history to a text file.

    Args:
        history: list of (user, bot) turns.
        filename: path to the history log file.
    """
    output_path = Path(filename)

    with output_path.open("a", encoding="utf-8") as convo:
        convo.write("\n=== Second Conversation ===\n\n")
        for user_msg, bot_msg in history:
            convo.write(f"User: {user_msg}\n")
            convo.write(f"Bot:  {bot_msg}\n\n")