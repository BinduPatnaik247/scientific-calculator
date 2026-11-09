#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -n "$(find . -name .git -print -quit)" ]; then
  echo 'FAIL: .git must not be included' >&2
  exit 1
fi
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
test "$(python3 -B -m calc_app add 0.1 0.2)" = '0.3'
test "$(python3 -B -m calc_app subtract 20 7)" = '13'
test "$(python3 -B -m calc_app multiply -2.5 4)" = '-10'
test "$(python3 -B -m calc_app divide 9 2)" = '4.5'
echo 'PASS: starter application checks'
