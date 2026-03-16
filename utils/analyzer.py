#!/usr/bin/env python3
"""
analyzer.py — Core password scoring and analysis logic.
"""

import re
import math
from utils.patterns import has_keyboard_pattern, has_repeated_chars
from utils.wordlist import is_common_password


def calculate_entropy(password: str) -> float:
    """
    Estimate password entropy in bits.
    Entropy = length * log2(character_pool_size)
    Higher entropy = harder to crack.
    """
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"\d", password):    pool += 10
    if re.search(r"[^a-zA-Z0-9]", password): pool += 32
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)


def estimate_crack_time(entropy: float) -> str:
    """
    Rough estimate of brute-force crack time at 1 billion guesses/second.
    """
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
    """
    Score a password from 0-100.
    Returns (score, passed_checks, failed_checks).
    """
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
        passed.append("Contains uppercase letters (+10)")
    else:
        failed.append("Add uppercase letters (A-Z)")

    if re.search(r"[a-z]", password):
        score += 10
        passed.append("Contains lowercase letters (+10)")
    else:
        failed.append("Add lowercase letters (a-z)")

    if re.search(r"\d", password):
        score += 10
        passed.append("Contains digits (+10)")
    else:
        failed.append("Add at least one digit (0-9)")

    if re.search(r"[^a-zA-Z0-9]", password):
        score += 15
        passed.append("Contains special characters (+15)")
    else:
        failed.append("Add special characters (!@#$%^&*)")

    # --- Common password check ---
    if is_common_password(password):
        failed.append("This is a very common password — change it!")
    else:
        score += 20
        passed.append("Not a common/leaked password (+20)")

    # --- Pattern checks ---
    if has_repeated_chars(password):
        failed.append("Avoid repeated characters (e.g. 'aaa', '111')")
    else:
        score += 5
        passed.append("No repeated character sequences (+5)")

    if has_keyboard_pattern(password):
        failed.append("Avoid keyboard patterns (e.g. 'qwerty', '12345')")
    else:
        score += 5
        passed.append("No keyboard walk patterns (+5)")

    return min(score, 100), passed, failed


def get_grade(score: int) -> str:
    if score >= 80: return "A"
    if score >= 60: return "B"
    if score >= 40: return "C"
    if score >= 20: return "D"
    return "F"


def get_label(score: int) -> str:
    if score >= 80: return "Very Strong"
    if score >= 60: return "Strong"
    if score >= 40: return "Moderate"
    if score >= 20: return "Weak"
    return "Very Weak"


def analyze_password(password: str) -> dict:
    """
    Full analysis of a password. Returns a result dictionary.
    """
    score, passed, failed = score_password(password)
    entropy = calculate_entropy(password)
    return {
        "password": password,
        "score": score,
        "grade": get_grade(score),
        "label": get_label(score),
        "entropy": round(entropy, 1),
        "crack_time": estimate_crack_time(entropy),
        "passed": passed,
        "failed": failed,
        "length": len(password),
    }
