import io
import os
import re
import sys
from pathlib import Path

os.system("")
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")

COMMIT_PATTERN = re.compile(r"^OPL-C00\d+\s\|\s(feat|fix|docs|chore|test):\s.+")
print("✅ Running commit message hook...")


def main():
    if len(sys.argv) < 2:
        print("Usage: check_commit_message.py <commit-msg-file>")
        sys.exit(1)
    commit_msg_file = Path(sys.argv[1])
    message = commit_msg_file.read_text(encoding="utf-8").strip()
    if not COMMIT_PATTERN.match(message):
        print("\n\033[1;37;41m[ERROR]\033[0m — Invalid commit message format!\n")
        print("Expected format:")
        print("  OPL-C00<number> | <commit-tag>: <description>")
        print("\nExample:")
        print("  OPL-C002 | chore: Adding pre-commit config and initial CI workflow\n")
        print("Your message:")
        print(f"  {message}\n")
        sys.exit(1)
    sys.exit(0)
    return True


if __name__ == "__main__":
    main()
