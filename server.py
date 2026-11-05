"""Tiny local web app. Run:  python3 server.py   then open http://localhost:8000
Uses only the Python standard library."""
import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from rules import analyze

HERE = os.path.dirname(os.path.abspath(__file__))
WATSON_FILE = os.path.join(HERE, "watson_results.json")  # written from the real IBM notebook run

def watson_for(text):
    """Return real IBM Watson NLP output for this exact text if we have it, else None.
    We never invent Watson results."""
    if not os.path.exists(WATSON_FILE):
        return None
    try:
        data = json.load(open(WATSON_FILE, encoding="utf-8"))
    except Exception:
        return None
    return data.get(text.strip())

KEYS = ("anger", "disgust", "fear", "joy", "sadness")

def import_watson(payload):
    """Accept the JSON printed by notebook_cell.py: {message: {"emotion": {anger..sadness}}}.
    Only well-formed numbers are stored, so nothing is invented or malformed."""
    if not isinstance(payload, dict) or not payload:
        raise ValueError("Expected a JSON object: {message: {emotion: {...}}}")
    data = {}
    if os.path.exists(WATSON_FILE):
        data = json.load(open(WATSON_FILE, encoding="utf-8"))
    added = 0
    for msg, v in payload.items():
        e = v.get("emotion") if isinstance(v, dict) else None
        if not isinstance(msg, str) or not isinstance(e, dict) or set(e) != set(KEYS):
            raise ValueError("Each entry needs an emotion with anger, disgust, fear, joy, sadness.")
        if not all(isinstance(e[k], (int, float)) and 0 <= e[k] <= 1 for k in KEYS):
            raise ValueError("Emotion scores must be numbers from 0 to 1.")
        data[msg.strip()] = {"emotion": {k: float(e[k]) for k in KEYS},
            "source": "IBM watson_nlp emotion_aggregated-workflow_en_stock, output copied from a watsonx.ai Studio notebook run"}
        added += 1
    json.dump(data, open(WATSON_FILE, "w", encoding="utf-8"), indent=1)
    return added

class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, open(os.path.join(HERE, "index.html"), "rb").read(), "text/html; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain")
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        if self.path == "/import":
            try:
                k = import_watson(json.loads(self.rfile.read(n) or b"{}"))
                return self._send(200, json.dumps({"ok": True, "added": k}).encode(), "application/json")
            except Exception as ex:
                return self._send(400, json.dumps({"ok": False, "error": str(ex)}).encode(), "application/json")
        if self.path != "/analyze":
            return self._send(404, b"not found", "text/plain")
        text = json.loads(self.rfile.read(n) or b"{}").get("text", "")
        out = analyze(text)
        w = watson_for(text)
        out["watson"] = w if w else {"status": "not_available",
            "note": "No IBM Watson NLP result saved for this exact message. Run it in the watsonx notebook (see README)."}
        self._send(200, json.dumps(out).encode(), "application/json")

if __name__ == "__main__":
    print("Open http://localhost:8000  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", 8000), H).serve_forever()
