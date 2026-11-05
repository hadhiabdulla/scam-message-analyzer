"""Held-out set written AFTER the rule changes, not used to tune rules. 1 = scam, 0 = normal.
Small and hand-written: it shows rough behaviour, it does not measure real-world accuracy."""
HELDOUT = [
 (1, "Dear customer, your debit card is blocked. Verify your card number and PIN at http://sbi-verify-kyc.top/login now."),
 (1, "Your Netflix payment failed. Update billing details at netflix-update-pay.xyz or your account will be suspended."),
 (1, "Pay the customs fee of Rs 1,850 via UPI to release your parcel, else it will be returned."),
 (1, "Work from home and make $300 per day, no experience needed. WhatsApp me to join."),
 (1, "You are selected for a free iPhone 15! Click http://192.168.4.7/claim to get it."),
 (1, "This is the tax department. Buy Google Play gift cards worth 20000 and send the codes to avoid arrest."),
 (1, "Hi, I am your boss. Need a quick favour, buy vouchers and message me the codes. Don't call."),
 (1, "Your electricity will be cut tonight. Call this number and share your account number to avoid disconnection."),
 (0, "Dinner at 8? I booked the table near the window."),
 (0, "Your bank statement for October is ready in the official app."),
 (0, "Your OTP is 551203. Never share this code with anyone."),
 (0, "Can you send me the notes from yesterday's class?"),
 (0, "Your flight 6E-204 is on time. Boarding starts at 5:10 PM."),
 (0, "Happy birthday! Let's get a gift for Riya, I will pay my share tomorrow."),
 (0, "Your account password was changed. If this was you, no action is needed."),
 (0, "Sale: 20% off at the store this weekend only."),
]
