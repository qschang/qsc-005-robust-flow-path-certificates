#!/bin/sh
set -eu
REWARD_FILE=/logs/verifier/reward.txt
REPORT=/logs/verifier/pytest-report.xml
mkdir -p "$(dirname "$REWARD_FILE")"
printf '0.000\n' > "$REWARD_FILE"
chmod 0444 "$REWARD_FILE" 2>/dev/null || true
cleanup() {
  code=$?
  chmod 0644 "$REWARD_FILE" 2>/dev/null || true
  complete=INCOMPLETE
  if [ "$code" -eq 0 ] && test -s "$REPORT"; then
    if grep -Eq '<testsuite[^>]*tests="12"[^>]*failures="0"[^>]*errors="0"[^>]*skipped="0"' "$REPORT"; then
      complete=COMPLETE
    fi
  fi
  if [ "$complete" = COMPLETE ]; then printf '1.000\n' > "$REWARD_FILE"; else printf '0.000\n' > "$REWARD_FILE"; fi
  chmod 0444 "$REWARD_FILE" 2>/dev/null || true
  exit "$code"
}
trap cleanup EXIT INT TERM HUP
python3 -m pip install --no-cache-dir --disable-pip-version-check pytest==8.4.2
timeout 240s python3 -m pytest -q "$(dirname "$0")/test_contract.py" --junitxml="$REPORT"
