#!/usr/bin/env python3
"""
patterns.py — Detect weak password patterns like keyboard walks and repeated chars.
"""

import re

# Common keyboard row sequences (and their reverses)
KEYBOARD_PATTERNS = [
    "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "1234567890", "qwerty", "asdfgh", "zxcvbn",
    "abcdef", "abcdefgh", "abcdefghij",
]


def has_keyboard_pattern(password: str) -> bool:
    """
    Return True if the password contains a keyboard walk pattern.
    e.g. 'qwerty', '12345', 'asdf'
    """
    lower = password.lower()
    for pattern in KEYBOARD_PATTERNS:
        # Check for any 4+ character substring of a keyboard row
        for i in range(len(pattern) - 3):
            chunk = pattern[i:i+4]
            if chunk in lower or chunk[::-1] in lower:
                return True
    return False


def has_repeated_chars(password: str) -> bool:
    """
    Return True if the password has 3+ repeated characters in a row.
    e.g. 'aaa', '111', '!!!', 'aaaa'
    """
    return bool(re.search(r"(.)\1{2,}", password))
