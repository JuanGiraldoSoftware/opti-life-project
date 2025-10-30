import os
import re
import sys
from pathlib import Path

os.system("")

DECORATOR_PATTERN = re.compile(r"^@app\.(get|post|put|delete|patch)\(.*\)\s*$")
DEF_PATTERN = re.compile(r"^def\s+[A-Za-z_]\w*\s*\(.*\):\s*$")
RETURN_PATTERN = re.compile(r"^\s*return\b")


def check_file(path: Path) -> bool:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    passed = True
    inside_endpoint = False
    last_return_line = -3
    func_indent = None

    for i, line in enumerate(lines):
        stripped = line.rstrip("\n")

        if DECORATOR_PATTERN.match(stripped.strip()):
            if last_return_line != -3:
                blank_lines_between = i - last_return_line - 1
                if blank_lines_between != 2:
                    print(
                        f"{path}:{i+1} \033[1;37;41m[ERROR]\033[0m — Endpoints must be separated by exactly TWO blank lines (found {blank_lines_between})"
                    )
                    passed = False
            continue

        if DEF_PATTERN.match(stripped.strip()):
            inside_endpoint = True
            func_indent = len(line) - len(line.lstrip(" "))
            continue

        if inside_endpoint:
            if stripped.strip() == "":
                print(
                    f"{path}:{i+1} \033[1;37;41m[ERROR]\033[0m — Blank line inside endpoint body not allowed"
                )
                passed = False

            if RETURN_PATTERN.match(stripped):
                inside_endpoint = False
                last_return_line = i
                func_indent = None

    return passed


def main():
    all_passed = True
    for filename in sys.argv[1:]:
        if not filename.endswith(".py"):
            continue
        if not check_file(Path(filename)):
            all_passed = False
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
