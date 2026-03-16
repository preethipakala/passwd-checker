#!/usr/bin/env python3
"""
wordlist.py — Load and query the common passwords list.
Passwords in this list should NEVER be used — they are the first
thing attackers try in a dictionary attack.
"""

import os

_WORDLIST_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "common_passwords.txt")
_common_passwords: set[str] = set()


def _load_wordlist():
    global _common_passwords
    if _common_passwords:
        return  # already loaded
    try:
        with open(_WORDLIST_PATH, "r") as f:
            _common_passwords = {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        _common_passwords = set()


def is_common_password(password: str) -> bool:
    """Return True if the password appears in the common passwords list."""
    _load_wordlist()
    return password.lower() in _common_passwords
