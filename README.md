# Scam Message Analyzer

Paste a suspicious message and get a risk level with plain-English reasons, the exact
warning signs highlighted in your text, batch checking for many messages at once, and a
private on-browser history.

**Live website:** hosted with GitHub Pages from this repo (see the repo's Pages settings).
The site is static: every check runs in your browser and nothing is sent anywhere.

## What's here
- `index.html`, `rules.js`, `watson-data.js` - the website (open `index.html` directly or via the Pages link).
- `rules.py` - the same rules in Python, used by the tests and the optional local server.
- `server.py` - optional small local server (`python3 server.py`, then http://localhost:8000). Not required: the website is fully static, but this also exposes `/analyze` and `/import` endpoints.
- `test_messages.py`, `heldout_messages.py`, `evaluate.py`, `evaluate_heldout.py` - test sets and runners.
- `parity_test.py` - proves the JS and Python rules give identical results on all test messages (needs node).
- `notebook_cell.py` - the watsonx.ai notebook cell for real IBM Watson NLP runs.
- `watson_results.json` - real saved IBM outputs (5 messages, two notebook runs on 5 Nov 2026).
- `evaluation_history_v1.txt`, `evaluation_heldout_v2.txt` - older results, kept honestly.

## Two separate parts, never mixed
1. **Our own rules** produce the risk score: urgency, OTP/PIN/card-detail requests, money
   asks, prizes, threats, shortened/IP/look-alike links, odd domain endings, gift cards,
   too-good earnings, shouting. Every matched rule shows the exact text it matched.
2. **IBM Watson NLP** (real, run by you in a watsonx.ai Studio notebook) describes the
   emotion of the text. It does NOT decide "scam" (a prize scam reads as "joy").

## Why Watson is not a live call on the website
There is no free always-on way for a public web page to call this IBM model:
- The model only runs inside a notebook runtime or a deployment. On the free Lite plan the
  notebook runtime costs about 6 capacity units per hour from a free 10 per month; an
  always-on deployment would exceed the free allowance in hours and then needs payment.
- Calling IBM from a public page would require putting the account API key in public
  client-side code, which would leak it. A server-side proxy means hosting and billing.

So the site keeps real notebook outputs, labels them "saved result, not a live call", and
makes the new-message path as short as possible:
1. Analyze your message on the site.
2. Press **Copy notebook cell for this message** (the cell is prepared with your text).
3. Run it in your watsonx.ai notebook (runtime "NLP + DO Runtime ... XS"; stop the runtime
   after - it bills about 6 CU/hour against the free 10/month).
4. Paste the printed JSON into **Add IBM Watson result**. The shape is checked before
   saving; results are stored only in your browser.

This path was tested end to end with a new message (a fake "Amazon order on hold" text):
real notebook run, copied output, saved in the app, shown as bars.

## Test results (`python3 evaluate.py`, `python3 evaluate_heldout.py`)
Hand-written messages (not real people's), small sets - a rough guide, not proof of
real-world accuracy.
- v1 rules, 20 development messages: 17/20 correct, 8/10 scams caught, 1/10 false alarm
  (`evaluation_history_v1.txt`).
- v2 rules (added card/login detail requests, gift cards, easy-money, look-alike links),
  same dev set: 19/20 (tuned on it, so this number means little).
- Held-out set of 16 written after the rule changes, not tuned on: 14/16 correct, 8/8
  scams caught, 2/8 genuine messages wrongly flagged (a real OTP notice and a "password
  was changed" notice) (`evaluation_heldout_v2.txt`). Left as is.
- `python3 parity_test.py`: 36/36 identical results between rules.js and rules.py.

A low score is shown as "Few warning signs - safety NOT established" (grey), never green
"safe". Rule-based checks miss new tricks and flag some real alerts. Never rely on this
alone; do not click links or share OTPs.

## Privacy
Checks run in your browser. History and imported Watson results are stored only in the
browser's local storage on your device; clearing site data removes them.
