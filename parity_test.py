"""Parity test: the browser rules (rules.js, via node) must give the same score, level and
matched rules as the Python rules (rules.py) on every test message.
Run:  python3 parity_test.py   (needs node on PATH)"""
import json, subprocess, sys
from rules import analyze
from test_messages import TESTS
from heldout_messages import HELDOUT

JS = """
const {analyze} = require('./rules.js');
const msgs = JSON.parse(require('fs').readFileSync(0, 'utf8'));
console.log(JSON.stringify(msgs.map(m => {
  const r = analyze(m);
  return {score: r.score, level: r.level, rules: r.signals.map(s => s.rule)};
})));
"""
msgs = [t for _, t in TESTS] + [t for _, t in HELDOUT]
js = json.loads(subprocess.run(["node", "-e", JS], input=json.dumps(msgs),
                               capture_output=True, text=True, check=True).stdout)
bad = 0
for m, j in zip(msgs, js):
    p = analyze(m)
    if p["score"] != j["score"] or p["level"] != j["level"] or [s["rule"] for s in p["signals"]] != j["rules"]:
        bad += 1
        print("MISMATCH:", m[:60], "| py", p["score"], "| js", j["score"])
print(f"parity: {len(msgs)-bad}/{len(msgs)} identical")
sys.exit(1 if bad else 0)
