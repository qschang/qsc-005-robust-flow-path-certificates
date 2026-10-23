#!/usr/bin/env python3
import sys, json, argparse
import xml.etree.ElementTree as ET

def main(path: str, report_out=None, reward_out=None, config_path=None) -> int:
    root = ET.parse(path).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        reward=0.0
        print("0.000")
        return 2
    attrs = suite.attrib
    cases={}
    for tc in suite.iter("testcase"):
        cls=tc.attrib.get("classname",""); nm=tc.attrib.get("name","")
        ok=not any(tc.find(tag) is not None for tag in ("failure","error","skipped"))
        cases[cls+"::"+nm]=ok; cases[cls.split('.')[-1]+".py::"+nm]=ok
    cfg=json.load(open(config_path,encoding='utf-8')) if config_path else None
    if cfg:
        gates=cfg.get('gate_tests',[]); tests=cfg.get('tests',{})
        gate_ok=all(cases.get(x,False) for x in gates)
        reward=sum(float(v['weight']) for k,v in tests.items() if cases.get(k,False)) if gate_ok else 0.0
        reward=round(reward,3)
    else:
        total = int(attrs.get("tests", "0")); bad = sum(int(attrs.get(k, "0")) for k in ("failures", "errors", "skipped")); reward=1.0 if total == 13 and bad == 0 else 0.0
    if report_out:
        with open(report_out,'w',encoding='utf-8') as f: json.dump({'status':'COMPLETED','reward':reward,'gate_passed':(not cfg or all(cases.get(x,False) for x in cfg.get('gate_tests',[])))},f)
    if reward_out:
        with open(reward_out,'w',encoding='utf-8') as f: f.write(f'{reward:.3f}\n')
    print(f'{reward:.3f}')
    return 0

if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument('path',nargs='?'); ap.add_argument('--config'); ap.add_argument('--junit'); ap.add_argument('--report-out'); ap.add_argument('--reward-out'); a=ap.parse_args()
    raise SystemExit(main(a.junit or a.path, a.report_out, a.reward_out, a.config) if (a.junit or a.path) else 2)
