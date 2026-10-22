#!/bin/sh
set -eu
reward_file=/logs/verifier/reward.txt
report=/logs/verifier/pytest-report.xml
mkdir -p "$(dirname "$reward_file")"
printf '0.000\n' > "$reward_file"
cleanup(){ code=$?; if [ "$code" -eq 0 ] && [ -s "$report" ]; then printf '1.000\n' > "$reward_file"; else printf '0.000\n' > "$reward_file"; fi; exit "$code"; }
trap cleanup EXIT INT TERM HUP
timeout 240s python3 -m pytest -q "$(dirname "$0")/test_contract.py" --junitxml="$report"
