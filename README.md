# 🔐 Password Strength Checker

A beginner-friendly Python CLI tool that analyzes how strong a password is using **real security criteria** — the same rules used by security professionals.

> 🛡️ Passwords are analyzed **locally only** — nothing is ever sent over the network.

---

## 📚 What You'll Learn

- What makes a password strong or weak
- How dictionary/common password attacks work
- Python string manipulation and regex basics
- How to build a useful security CLI tool

---

## 🛠️ Features

- ✅ Scores passwords from 0–100 with a letter grade (A–F)
- ✅ Checks length, uppercase, lowercase, digits, and symbols
- ✅ Detects common/leaked passwords (top 1000 list)
- ✅ Detects repeated characters and keyboard patterns (e.g. `qwerty`, `12345`)
- ✅ Estimates crack time (brute-force estimate)
- ✅ Gives actionable improvement tips
- ✅ Supports batch mode — check a list of passwords from a file

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/preethipakala/passwd-checker.git
cd passwd-checker
```

### 2. Check a single password (interactive)
```bash
python checker.py
```

### 3. Check a password directly
```bash
python checker.py --password "MyP@ssw0rd!"
```

### 4. Batch check from a file (one password per line)
```bash
python checker.py --file passwords.txt
```

### 5. Output results to a report
```bash
python checker.py --file passwords.txt --output report.txt
```

---

## 📊 Scoring Criteria

| Check                        | Points |
|------------------------------|--------|
| Length ≥ 8                   | +10    |
| Length ≥ 12                  | +15    |
| Length ≥ 16                  | +20    |
| Uppercase letters            | +10    |
| Lowercase letters            | +10    |
| Digits                       | +10    |
| Special characters           | +15    |
| Not a common password        | +20    |
| No repeated chars (aaa)      | +5     |
| No keyboard patterns         | +5     |

**Grades:** A (80–100) · B (60–79) · C (40–59) · D (20–39) · F (0–19)

---

## 📁 Project Structure

```
passwd-checker/
├── checker.py          # Main CLI entry point
├── utils/
│   ├── __init__.py
│   ├── analyzer.py     # Core scoring logic
│   ├── patterns.py     # Keyboard/repeat pattern detection
│   └── wordlist.py     # Common password list + lookup
├── data/
│   └── common_passwords.txt   # Top 1000 common passwords
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔭 Next Steps / Ideas

- [ ] Add entropy calculation (bits of entropy)
- [ ] Add color-coded terminal output
- [ ] Add `--verbose` flag for detailed breakdown
- [ ] Integrate with HaveIBeenPwned API (check if password was leaked)
- [ ] Build a simple web UI with Flask

---

## 📜 License

MIT License — free to use, modify, and learn from.
