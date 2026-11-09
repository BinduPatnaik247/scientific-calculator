# Python Calculator — starter project

A working command-line application for addition, subtraction, multiplication,
and division. This is the basic application; the larger enhancement is a separate
assignment. 

Requirements and run commands

Linux with Python 3.10 or newer. Only the Python standard library is used. No pip
install, network access, database, or API key is needed for the starter.

```bash
cd calculator\\\_project
python3 -m calc\\\_app --help
python3 -m calc\\\_app add 10 5
# 15
python3 -m calc\\\_app subtract 10 5
# 5
python3 -m calc\\\_app multiply -2.5 4
# -10
python3 -m calc\\\_app divide 10 4 --json
# {"operation": "divide", "left": "10", "right": "4", "result": "2.5"}
python3 -m calc\\\_app add 0.1 0.2
# 0.3
```

Decimal arithmetic uses 28 significant digits and half-even rounding. Numeric
inputs have at most 200 characters; nonzero input magnitude must be between
1e-100 and 1e100 inclusive. Nonfinite values are rejected. Results are fixed-point
strings with insignificant fractional zeros removed. Repeating decimals round
at the selected precision. Basic results may exceed input magnitude limits.

Exit code 0 means success; 2 means invalid input or a domain/usage error.
`--json` appears after the operation and makes calculation results/errors JSON.
Argparse syntax errors retain their normal stderr usage message. To pass a
negative scientific literal that argparse might treat as a flag, put `--json`
before `--`, e.g. `python3 -m calc\\\_app add --json -- -1e2 3`.

## Judge the basic task

```bash
bash scripts/verify\\\_basic.sh
```

Expected: 18 unit tests pass, the arithmetic smoke checks pass, exit code 0,
and `PASS: starter application checks`. The script also rejects any `.git` entry.

To check error handling directly:

```bash
python3 -m calc\\\_app divide 10 0 --json
echo "$?"
# {"error": "Cannot divide by zero."}
# 2
```

## Files

```text
calculator\\\_project/
  calc\\\_app/                 application package and CLI entry point
  tests/                    baseline unit and CLI tests
  scripts/verify\\\_basic.sh    Linux baseline verification
   README.md
```

The downloadable archive excludes `.git`, environments, caches, and databases.
No Git repository was initialized. Running without Python's `-B` option may
create normal `\\\_\\\_pycache\\\_\\\_` files locally; exclude these when repackaging.

