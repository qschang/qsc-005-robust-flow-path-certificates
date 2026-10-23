#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

def main(path: str) -> int:
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        print("0.000")
        return 2
    attrs = suite.attrib
    total = int(attrs.get("tests", "0"))
    bad = sum(int(attrs.get(k, "0")) for k in ("failures", "errors", "skipped"))
    print("1.000" if total == 13 and bad == 0 else "0.000")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]) if len(sys.argv) == 2 else 2)
