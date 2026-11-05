from rules import analyze
from test_messages import TESTS
tp=fp=tn=fn=0
print(f"{'label':5} {'score':5} {'verdict':11} message")
for label,text in TESTS:
    r=analyze(text); pred = 1 if r["score"]>=25 else 0
    tp+=label==1 and pred==1; fn+=label==1 and pred==0; fp+=label==0 and pred==1; tn+=label==0 and pred==0
    flag = "" if pred==label else "  <-- WRONG"
    print(f"{label:<5} {r['score']:<5} {r['level']:<11} {text[:70]}{flag}")
print(f"\ncorrect {tp+tn}/{len(TESTS)}  caught scams {tp}/{tp+fn}  false alarms {fp}/{fp+tn}")
