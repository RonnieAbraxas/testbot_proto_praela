"""
testbot.py

Entry point for the TestBot application.
Right now it only launches the CLI interface.
Later, we can add flags or subcommands (e.g. `--cli`, `--server`).
"""

from app.cli import run_cli


if __name__ == "__main__":
    run_cli()