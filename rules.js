/* Own rule-based scam signals. No AI service here: plain, explainable checks.
   This is the browser port of rules.py - keep the two in sync (parity test: parity_test.py).
   Each rule has a name, a weight, and a plain-English reason shown to the user. */
"use strict";

const URGENT = "\\b(urgent|immediately|right now|within \\d+ ?(hours?|hrs?|minutes?|mins?)|last chance|act now|expires? (today|soon)|final (notice|warning)|today only)\\b";
const MONEY_ASK = "\\b(send|transfer|pay|deposit)\\b.{0,40}\\b(fee|charge|tax|amount|money|rs\\.?|inr|usd|\\$|\u20B9|upi|gift ?card|bitcoin|crypto)\\b";
const SECRET_ASK = "\\b(otp|one[- ]time (password|code)|pin|cvv|password|passcode|card number|aadhaar|pan (number|card)|account number|login details?)\\b";
const PRIZE = "\\b(you (have )?won|winner|lottery|lucky draw|prize|reward|cashback|free (gift|iphone|recharge)|congratulations)\\b";
const THREAT = "\\b(suspend(ed)?|blocked|deactivat(ed|e)|legal action|arrest|penalty|freeze|frozen|kyc (expired|update|pending)|account will be closed)\\b";
const IMPERSONATE = "\\b(bank|sbi|hdfc|icici|paytm|amazon|flipkart|income tax|customs|courier|fedex|dhl|india post|police|telecom|trai|support team|customer care)\\b";
const SHORTENER = "\\b(bit\\.ly|tinyurl\\.com|t\\.co|goo\\.gl|cutt\\.ly|rb\\.gy|is\\.gd|shorturl\\.at)/\\S+";
const URLP = "(https?://\\S+|www\\.\\S+)";
const IP_URL = "https?://\\d{1,3}(\\.\\d{1,3}){3}";
const ODD_TLD = "https?://[^\\s/]+\\.(xyz|top|click|buzz|icu|live|work|cfd|sbs)\\b";

const CARD_ASK = "\\b(confirm|verify|update|enter|share|send|provide|re-?enter)\\b.{0,40}\\b(card|debit|credit|bank|payment|billing|login|account|identity|kyc)( (details?|info|information|number|credentials?))?\\b";
const GIFT_CARD = "\\b(gift ?cards?|itunes|google play card|steam card|vouchers?)\\b";
const EARN = "\\b(earn|make|get)\\b.{0,25}\\b(rs\\.?|inr|\\$|\u20B9|usd)\\s?\\d[\\d,]*\\s?(/|per |a |every )?(day|daily|week|weekly|hour|hourly)|\\b(work from home|guaranteed (income|returns?)|double your money)\\b";
const LINK_LOOKALIKE = "https?://[^\\s/]*(secure|verify|login|pay|update|kyc|account)[^\\s/]*-[^\\s/]*|https?://[^\\s/]*-(secure|verify|login|pay|update|kyc)[^\\s/]*";

const RULES = [
  ["asks_card_or_login_details", 30, CARD_ASK, "Asks you to confirm or enter card, bank or login details. Real companies do not ask this by message."],
  ["gift_card_mention", 25, GIFT_CARD, "Mentions gift cards or vouchers. Gift cards are a favourite way for scammers to get paid."],
  ["too_good_earnings", 25, EARN, "Promises easy money or fixed earnings. Real jobs do not promise this."],
  ["lookalike_link", 20, LINK_LOOKALIKE, "The link name mixes words like secure/pay/verify with dashes, a common look-alike trick."],
  ["urgency", 15, URGENT, "Pushes you to act fast, so you do not stop to think."],
  ["asks_for_secret", 30, SECRET_ASK, "Mentions an OTP, PIN, password or ID number. Real banks never ask you to share these."],
  ["asks_for_money", 20, MONEY_ASK, "Asks you to send or pay money for something you did not request."],
  ["prize_or_reward", 20, PRIZE, "Says you won or get a free reward. Unexpected prizes are a common trick."],
  ["threat", 20, THREAT, "Threatens that your account or service will be blocked or closed."],
  ["shortened_link", 20, SHORTENER, "Uses a shortened link that hides where it really goes."],
  ["ip_address_link", 25, IP_URL, "The link is a raw IP address, not a normal website name."],
  ["odd_link_ending", 15, ODD_TLD, "The link ends in an unusual domain (like .xyz or .top) often used for throwaway sites."],
];

function analyze(text) {
  const t = text || "";
  const low = t.toLowerCase();
  const hits = [];
  let score = 0;
  for (const [name, weight, pattern, why] of RULES) {
    const m = low.match(new RegExp(pattern, "is"));
    if (m) {
      hits.push({ rule: name, weight: weight, matched: m[0].slice(0, 60), why: why });
      score += weight;
    }
  }
  // Impersonation only counts when combined with a link, a threat or a request.
  const impM = low.match(new RegExp(IMPERSONATE, "i"));
  if (impM && (new RegExp(URLP, "i").test(low) || hits.some(h => ["threat", "asks_for_secret", "asks_for_money"].includes(h.rule)))) {
    hits.push({ rule: "impersonation", weight: 10, matched: impM[0], why: "Claims to be a known organisation while also pushing a link or a request." });
    score += 10;
  }
  const letters = [...t].filter(c => /[a-zA-Z]/.test(c));
  if (letters.length >= 20 && letters.filter(c => c >= "A" && c <= "Z").length / letters.length > 0.6) {
    hits.push({ rule: "shouting", weight: 5, matched: "mostly CAPITAL LETTERS", why: "Shouting in capitals is common in scam messages." });
    score += 5;
  }
  score = Math.min(score, 100);
  const level = score >= 50 ? "High risk" : score >= 25 ? "Suspicious" : (score === 0 ? "No rule matched - safety NOT established" : "Few warning signs - safety NOT established");
  return { score: score, level: level, signals: hits };
}

/* Highlight support: return [start, end) spans in the ORIGINAL text for every matched signal.
   Lowercase copy keeps the same offsets, so matches map back to the original text. */
function analyzeSpans(text) {
  const t = text || "";
  const low = t.toLowerCase();
  const spans = [];
  for (const [name, weight, pattern, why] of RULES) {
    const m = low.match(new RegExp(pattern, "is"));
    if (m) spans.push([m.index, m.index + m[0].length, name]);
  }
  const impM = low.match(new RegExp(IMPERSONATE, "i"));
  if (impM && (new RegExp(URLP, "i").test(low) || spans.some(s => ["threat", "asks_for_secret", "asks_for_money"].includes(s[2])))) {
    spans.push([impM.index, impM.index + impM[0].length, "impersonation"]);
  }
  return spans;
}

if (typeof module !== "undefined" && module.exports) module.exports = { analyze, analyzeSpans, RULES };
