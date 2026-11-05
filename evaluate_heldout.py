from rules import analyze
from heldout_messages import HELDOUT
tp=fn=fp=tn=0
for l,t in HELDOUT:
    r=analyze(t);p=r["score"]>=25
    tp+=l and p;fn+=l and not p;fp+=(not l) and p;tn+=(not l) and not p
    print(l,r["score"],"" if p==bool(l) else "<-- WRONG",t[:70])
print(f"correct {tp+tn}/{len(HELDOUT)} scams caught {tp}/{tp+fn} false alarms {fp}/{fp+tn}")
