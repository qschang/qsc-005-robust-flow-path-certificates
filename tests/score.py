#!/usr/bin/env python3
import sys, json, argparse
import xml.etree.ElementTree as ET

def main(path: str, report_out=None, reward_out=None) -> int:
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        reward=0.0
        print("0.000")
        return 2
    attrs = suite.attrib
    total = int(attrs.get("tests", "0"))
    bad = sum(int(attrs.get(k, "0")) for k in ("failures", "errors", "skipped"))
    reward=1.0 if total == 13 and bad == 0 else 0.0
    if report_out:
        with open(report_out,'w',encoding='utf-8') as f: json.dump({'status':'COMPLETED','reward':reward},f)
    if reward_out:
        with open(reward_out,'w',encoding='utf-8') as f: f.write(f'{reward:.3f}\n')
    print(f'{reward:.3f}')
    return 0

if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument('path',nargs='?'); ap.add_argument('--config'); ap.add_argument('--junit'); ap.add_argument('--report-out'); ap.add_argument('--reward-out'); a=ap.parse_args()
    raise SystemExit(main(a.junit or a.path, a.report_out, a.reward_out) if (a.junit or a.path) else 2)
