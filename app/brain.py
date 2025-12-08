"""
brain.py

This module contains TestBot's "brain" — the logic that generates
a reply given the user's message and (optionally) conversation history.

For now, it's a simple echo. Later, this will call a real LLM and
handle things like:
- safety / ethicist checks
- retrieval from Praela's knowledge bases
- personality conditioning
"""

from typing import List, Tuple


ConversationTurn = Tuple[str, str]  # (user, bot)
ConversationHistory = List[ConversationTurn]


def generate_reply(user_message: str, history: ConversationHistory) -> str:
    """
    Very first placeholder brain.

    Args:
        user_message: latest message from the user.
        history: list of (user, bot) turns so far in the conversation.

    Returns:
        A reply string.
    """
    # For now, we just mirror the user with a little prefix.
    # This is where we'll call an LLM later.
    return f"I heard you say: {user_message}"