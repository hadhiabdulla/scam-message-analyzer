# Scam Message Analyzer

Paste a suspicious message and get a risk level with plain-English reasons.

Two separate parts, never mixed:
1. **Our own rules** (`rules.py`): checks for urgency, asking for OTP/PIN, asking for money, prizes, threats, shortened or IP links, odd domains, shouting. This produces the risk score.
2. **IBM Watson NLP** (real, run in a watsonx.ai Studio notebook): describes the emotion of the text. It does NOT decide "scam".

## Run the app (no install, Python 3 only)
    python3 server.py
Open http://localhost:8000 and paste a message.

## About the Watson results (be clear on this)
`watson_results.json` holds output from one real notebook run (5 Nov 2026, model `emotion_aggregated-workflow_en_stock`) for 4 sample messages. The app shows it only for those exact messages and labels it "saved result". For any other message it says "not available". It is not a live call.

To get Watson output for your own messages:
1. Create a free IBM Cloud trial account, open watsonx.ai, create a project.
2. New asset > Jupyter notebook, runtime "NLP + DO Runtime XS" (uses 6 capacity units/hour of the free 10/month, so stop the runtime when done: project > Manage > Environments > Stop).
3. Paste `notebook_cell.py`, put your message in `MESSAGES`, run it, and copy the one line of JSON it prints.
4. In the app, open "Add IBM Watson result from your notebook", paste it, press Save. The app checks the shape and only then stores it. Analyze the same message again to see the Watson card.

This import path was tested end to end with a new message (a fake "Amazon order on hold" text): real notebook run, copied output, saved through the app, shown as bars. It is a manual step, not a live API.

## Test results (`python3 evaluate.py`)
20 hand-written messages (10 scam-like, 10 normal, some tricky; not real people's messages). Rules were not tuned to these tests.
- 17/20 correct. 8/10 scams caught. 1/10 normal flagged (a genuine bank OTP notice, because it mentions OTP).
- Missed: a "legal action, pay with gift cards" message and an "earn Rs 5000 daily" message (few trigger words).
- Small test set: treat these numbers as a rough guide, not proof. A rule-based checker will miss new tricks and flag some real alerts. Never rely on it alone; do not click links or share OTPs.

Watson emotion alone does not separate scams from normal text (a prize scam scored high "joy", like a friendly message), which is why it is shown as context only.

## Rules update and evaluation history (kept, not hidden)
- v1 (first rules), 20 development messages: 17/20 correct, 8/10 scams caught, 1/10 false alarm. Saved in `evaluation_history_v1.txt`.
- A new test message (fake Amazon "confirm your card details at amzn-secure-pay.top") scored only 15/100 and was labelled "Low risk". That was a real miss.
- v2 added rules for: card/bank/login detail requests, gift cards or vouchers, easy-money promises, look-alike links. Development set after changes: 19/20 (tuned on those messages, so this number means little).
- Held-out set written after the changes, not used for tuning (`heldout_messages.py`, `evaluation_heldout_v2.txt`): 14/16 correct, 8/8 scams caught, 2/8 normal messages wrongly flagged (a genuine OTP notice and a "password was changed" notice). These were left as is.
- 16 and 20 hand-written messages do not measure real-world accuracy. Expect both misses and false alarms.
- A low score is shown as "Few warning signs - safety NOT established" (grey), never as green "safe". Zero rules matching does not mean a message is safe.
