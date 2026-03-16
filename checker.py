#!/usr/bin/env python3
"""
Password Strength Checker
Analyze how strong a password is using real security criteria.

Usage:
    python checker.py                          # Interactive mode
    python checker.py --password "MyP@ss!"    # Check a single password
    python checker.py --file passwords.txt    # Batch check from file
    python checker.py --file passwords.txt --output report.txt
"""

import argparse
import sys
import getpass
from utils.analyzer import analyze_password
from utils.reporter import print_result, print_batch_summary, save_report


def interactive_mode():
    """Prompt the user to enter a password securely (hidden input)."""
    print("\n🔐 Password Strength Checker")
    print("─" * 40)
    password = getpass.getpass("  Enter password (hidden): ")
    if not password:
        print("[!] No password entered.")
        sys.exit(1)
    result = analyze_password(password)
    print_result(result)


def single_mode(password: str):
    """Analyze a single password passed via CLI argument."""
    result = analyze_password(password)
    print_result(result)


def batch_mode(filepath: str, output: str | None):
    """Read passwords from a file and analyze each one."""
    try:
        with open(filepath, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {filepath}")
        sys.exit(1)

    print(f"\n🔐 Batch Password Check — {len(passwords)} password(s) found\n")
    results = []
    for pw in passwords:
        result = analyze_password(pw)
        print_result(result, mask=True)
        results.append(result)

    print_batch_summary(results)

    if output:
        save_report(results, output)
        print(f"\n[✓] Report saved to: {output}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="🔐 Password Strength Checker — Learn what makes passwords secure"
    )
    parser.add_argument("--password", type=str, help="Password to check")
    parser.add_argument("--file",     type=str, help="Path to file with one password per line")
    parser.add_argument("--output",   type=str, help="Save batch results to a report file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.file:
        batch_mode(args.file, args.output)
    elif args.password:
        single_mode(args.password)
    else:
        interactive_mode()
