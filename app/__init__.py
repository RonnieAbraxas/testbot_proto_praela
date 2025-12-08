"""
app package

This package contains the core components of TestBot:
- brain: reply generation logic (eventually backed by a real LLM)
- cli:   command-line interface loop and history handling
"""

# Re-export convenience imports if we ever want them:
from .brain import generate_reply  # noqa: F401