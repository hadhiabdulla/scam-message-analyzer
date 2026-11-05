"""Own rule-based scam signals. No AI service here: plain, explainable checks.
Each rule has a name, a weight, and a plain-English reason shown to the user."""
import re

URGENT = r"\b(urgent|immediately|right now|within \d+ ?(hours?|hrs?|minutes?|mins?)|last chance|act now|expires? (today|soon)|final (notice|warning)|today only)\b"
MONEY_ASK = r"\b(send|transfer|pay|deposit)\b.{0,40}\b(fee|charge|tax|amount|money|rs\.?|inr|usd|\$|₹|upi|gift ?card|bitcoin|crypto)\b"
SECRET_ASK = r"\b(otp|one[- ]time (password|code)|pin|cvv|password|passcode|card number|aadhaar|pan (number|card)|account number|login details?)\b"
PRIZE = r"\b(you (have )?won|winner|lottery|lucky draw|prize|reward|cashback|free (gift|iphone|recharge)|congratulations)\b"
THREAT = r"\b(suspend(ed)?|blocked|deactivat(ed|e)|legal action|arrest|penalty|freeze|frozen|kyc (expired|update|pending)|account will be closed)\b"
IMPERSONATE = r"\b(bank|sbi|hdfc|icici|paytm|amazon|flipkart|income tax|customs|courier|fedex|dhl|india post|police|telecom|trai|support team|customer care)\b"
SHORTENER = r"\b(bit\.ly|tinyurl\.com|t\.co|goo\.gl|cutt\.ly|rb\.gy|is\.gd|shorturl\.at)/\S+"
URL = r"(https?://\S+|www\.\S+)"
IP_URL = r"https?://\d{1,3}(\.\d{1,3}){3}"
ODD_TLD = r"https?://[^\s/]+\.(xyz|top|click|buzz|icu|live|work|cfd|sbs)\b"

CARD_ASK = r"\b(confirm|verify|update|enter|share|send|provide|re-?enter)\b.{0,40}\b(card|debit|credit|bank|payment|billing|login|account|identity|kyc)( (details?|info|information|number|credentials?))?\b"
GIFT_CARD = r"\b(gift ?cards?|itunes|google play card|steam card|vouchers?)\b"
EARN = r"\b(earn|make|get)\b.{0,25}\b(rs\.?|inr|\$|₹|usd)\s?\d[\d,]*\s?(/|per |a |every )?(day|daily|week|weekly|hour|hourly)|\b(work from home|guaranteed (income|returns?)|double your money)\b"
LINK_LOOKALIKE = r"https?://[^\s/]*(secure|verify|login|pay|update|kyc|account)[^\s/]*-[^\s/]*|https?://[^\s/]*-(secure|verify|login|pay|update|kyc)[^\s/]*"
RULES = [
    ("asks_card_or_login_details", 30, CARD_ASK, "Asks you to confirm or enter card, bank or login details. Real companies do not ask this by message."),
    ("gift_card_mention", 25, GIFT_CARD, "Mentions gift cards or vouchers. Gift cards are a favourite way for scammers to get paid."),
    ("too_good_earnings", 25, EARN, "Promises easy money or fixed earnings. Real jobs do not promise this."),
    ("lookalike_link", 20, LINK_LOOKALIKE, "The link name mixes words like secure/pay/verify with dashes, a common look-alike trick."),
    ("urgency", 15, URGENT, "Pushes you to act fast, so you do not stop to think."),
    ("asks_for_secret", 30, SECRET_ASK, "Mentions an OTP, PIN, password or ID number. Real banks never ask you to share these."),
    ("asks_for_money", 20, MONEY_ASK, "Asks you to send or pay money for something you did not request."),
    ("prize_or_reward", 20, PRIZE, "Says you won or get a free reward. Unexpected prizes are a common trick."),
    ("threat", 20, THREAT, "Threatens that your account or service will be blocked or closed."),
    ("shortened_link", 20, SHORTENER, "Uses a shortened link that hides where it really goes."),
    ("ip_address_link", 25, IP_URL, "The link is a raw IP address, not a normal website name."),
    ("odd_link_ending", 15, ODD_TLD, "The link ends in an unusual domain (like .xyz or .top) often used for throwaway sites."),
]

def analyze(text):
    t = text or ""
    low = t.lower()
    hits, score = [], 0
    for name, weight, pattern, why in RULES:
        m = re.search(pattern, low, re.I | re.S)
        if m:
            hits.append({"rule": name, "weight": weight, "matched": m.group(0)[:60], "why": why})
            score += weight
    # Impersonation only counts when combined with a link, a threat or a request.
    if re.search(IMPERSONATE, low) and (re.search(URL, low) or any(h["rule"] in ("threat", "asks_for_secret", "asks_for_money") for h in hits)):
        m = re.search(IMPERSONATE, low)
        hits.append({"rule": "impersonation", "weight": 10, "matched": m.group(0), "why": "Claims to be a known organisation while also pushing a link or a request."})
        score += 10
    letters = [c for c in t if c.isalpha()]
    if len(letters) >= 20 and sum(c.isupper() for c in letters) / len(letters) > 0.6:
        hits.append({"rule": "shouting", "weight": 5, "matched": "mostly CAPITAL LETTERS", "why": "Shouting in capitals is common in scam messages."})
        score += 5
    score = min(score, 100)
    level = "High risk" if score >= 50 else "Suspicious" if score >= 25 else ("No rule matched - safety NOT established" if score == 0 else "Few warning signs - safety NOT established")
    return {"score": score, "level": level, "signals": hits}
