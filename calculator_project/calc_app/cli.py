"""CLI adapter. Future enhancements should reuse the arithmetic core."""

import argparse
import json
import sys

from . import __version__
from .core import OPERATIONS, CalculationError, calculate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Basic decimal calculator")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in OPERATIONS:
        command = commands.add_parser(name, help=f"{name.capitalize()} two numbers")
        command.add_argument("left")
        command.add_argument("right")
        command.add_argument("--json", action="store_true", help="Print a JSON response")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = calculate(args.command, args.left, args.right)
    except CalculationError as exc:
        if args.json:
            print(json.dumps({"error": str(exc)}))
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"operation": args.command, "left": args.left,
                          "right": args.right, "result": result}))
    else:
        print(result)
    return 0
