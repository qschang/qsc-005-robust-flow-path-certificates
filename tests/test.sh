#!/bin/sh
set -eu
reward_file=/logs/verifier/reward.txt
report=/logs/verifier/pytest-report.xml
mkdir -p "$(dirname "$reward_file")"
printf '0.000\n' > "$reward_file"
chmod 0444 "$reward_file" 2>/dev/null || true
cleanup() {
  code=$?
  chmod 0644 "$reward_file" 2>/dev/null || true
  if [ "$code" -eq 0 ] && [ -s "$report" ] && python3 - "$report" <<'PY'
import sys, xml.etree.ElementTree as ET
root=ET.parse(sys.argv[1]).getroot()
assert root.attrib.get("tests") == "11"
assert root.attrib.get("failures", "0") == "0"
assert root.attrib.get("errors", "0") == "0"
assert root.attrib.get("skipped", "0") == "0"
PY
  then printf '1.000\n' > "$reward_file"; else printf '0.000\n' > "$reward_file"; fi
  chmod 0444 "$reward_file" 2>/dev/null || true
  exit "$code"
}
trap cleanup EXIT INT TERM HUP
# Run the discoverable behavior suite and preserve its structured completion report.
timeout 240s python3 -m pytest -q "$(dirname "$0")/test_contract.py" --junitxml="$report"
