#!/usr/bin/env python3
"""
reporter.py — Terminal output and report generation.
"""

from datetime import datetime

GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

GRADE_COLORS = {
    "A": GREEN,
    "B": GREEN,
    "C": YELLOW,
    "D": YELLOW,
    "F": RED,
}

GRADE_BARS = {
    "A": "██████████",
    "B": "████████░░",
    "C": "██████░░░░",
    "D": "████░░░░░░",
    "F": "██░░░░░░░░",
}


def _mask(password: str) -> str:
    """Show first and last char only, mask the rest."""
    if len(password) <= 2:
        return "*" * len(password)
    return password[0] + "*" * (len(password) - 2) + password[-1]


def print_result(result: dict, mask: bool = False):
    """Pretty-print a single password analysis result."""
    pw_display = _mask(result["password"]) if mask else result["password"]
    grade  = result["grade"]
    color  = GRADE_COLORS.get(grade, RESET)
    bar    = GRADE_BARS.get(grade, "")

    print(f"\n{CYAN}{'─' * 50}{RESET}")
    print(f"  Password : {BOLD}{pw_display}{RESET}  (length: {result['length']})")
    print(f"  Score    : {color}{BOLD}{result['score']}/100{RESET}  [{bar}]  Grade: {color}{BOLD}{grade}{RESET}")
    print(f"  Strength : {color}{result['label']}{RESET}")
    print(f"  Entropy  : {result['entropy']} bits")
    print(f"  Crack est: {result['crack_time']}")

    if result["passed"]:
        print(f"\n  {GREEN}✓ Passed:{RESET}")
        for p in result["passed"]:
            print(f"    + {p}")

    if result["failed"]:
        print(f"\n  {RED}✗ Improve:{RESET}")
        for f in result["failed"]:
            print(f"    - {f}")

    print(f"{CYAN}{'─' * 50}{RESET}")


def print_batch_summary(results: list):
    """Print a summary table after a batch check."""
    print(f"\n{BOLD}{'─' * 50}")
    print(f"  Batch Summary — {len(results)} passwords")
    print(f"{'─' * 50}{RESET}")
    grades = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for r in results:
        grades[r["grade"]] += 1
    for grade, count in grades.items():
        color = GRADE_COLORS[grade]
        bar = "█" * count
        print(f"  Grade {color}{grade}{RESET}: {bar} ({count})")
    avg = sum(r["score"] for r in results) / len(results) if results else 0
    print(f"\n  Average score: {avg:.1f}/100")


def save_report(results: list, filename: str):
    """Save batch results to a text file."""
    with open(filename, "w") as f:
        f.write("Password Strength Report\n")
        f.write("========================\n")
        f.write(f"Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total   : {len(results)} passwords\n\n")
        for r in results:
            f.write(f"Password : {_mask(r['password'])}\n")
            f.write(f"Score    : {r['score']}/100  Grade: {r['grade']}  ({r['label']})\n")
            f.write(f"Entropy  : {r['entropy']} bits\n")
            f.write(f"Crack est: {r['crack_time']}\n")
            if r["failed"]:
                f.write("  Issues : " + "; ".join(r["failed"]) + "\n")
            f.write("\n")
