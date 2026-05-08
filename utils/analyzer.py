#!/usr/bin/env python3
"""analyzer.py — Core password scoring and analysis logic.""

import re
import math
from utils.patterns import has_keyboard_pattern, has_repeated_chars
from utils.wordlist import is_common_password


def calculate_entropy(password: str) -> float:
    """Estimate password entropy in bits."
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"\d", password): pool += 10
    if re.search(r"[^a-zA-Z0-9]", password): pool += 32
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def estimate_crack_time(entropy: float) -> str:
    """Rough estimate of brute-force crack time."
    seconds = (2 ** entropy) / 1_000_000_000
    if seconds < 1:
        return "instantly"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    elif seconds < 3.154e9:
        return f"{seconds/31536000:.1f} years"
    else:
        return "centuries"


def score_password(password: str) -> tuple[int, list[str], list[str]]:
    """Score a password from 0-100."
    score = 0
    passed = []
    failed = []

    # --- Length checks ---
    if len(password) >= 16:
        score += 20
        passed.append("Length ≥ 16 characters (+20)")
    elif len(password) >= 12:
        score += 15
        passed.append("Length ≥ 12 characters (+15)")
    elif len(password) >= 8:
        score += 10
        passed.append("Length ≥ 8 characters (+10)")
    else:
        failed.append("Too short — use at least 8 characters")

    # --- Character variety ---
    if re.search(r"[A-Z]", password):
        score += 10
        passed.append("Uppercase letters (+10)")
    if re.search(r"[a-z]", password):
        score += 10
        passed.append("Lowercase letters (+10)")
    if re.search(r"\d", password):
        score += 10
        passed.append("Digits (+10)")
    if re.search(r"[^a-zA-Z0-9]", password):
        score += 15
        passed.append("Special characters (+15)")

    # --- Common passwords ---
    if not is_common_password(password):
        score += 20
        passed.append("Not a common password (+20)")

    # --- Repeated patterns ---
    if not has_repeated_chars(password):
        score += 5
        passed.append("No repeated characters (+5)")
    if not has_keyboard_pattern(password):
        score += 5
        passed.append("No keyboard pattern (+5)")

    return min(score, 100), passed, failed

