"""Hand-written test messages. Written by the project author for testing, NOT real
people's messages. label: 1 = scam-like, 0 = normal. Includes tricky ones on purpose."""
TESTS = [
 # scam-like
 (1, "URGENT: Your SBI account will be blocked today. Update KYC now at http://sbi-kyc-update.xyz/login"),
 (1, "Congratulations! You have won Rs. 25,00,000 in the lucky draw. Send Rs. 2,500 processing fee to claim your prize."),
 (1, "Dear customer, share the OTP you received to avoid account suspension. Customer care team"),
 (1, "Your parcel is held at customs. Pay a small fee at bit.ly/3xYpay within 24 hours or it will be returned."),
 (1, "Income Tax refund of Rs 18,420 approved. Verify your account number and PAN at http://203.0.113.9/refund"),
 (1, "FINAL WARNING!!! YOUR PAYTM WALLET IS FROZEN. CLICK TO REACTIVATE AND ENTER YOUR PIN."),
 (1, "You have been selected for a free iPhone. Act now, only today: tinyurl.com/free-iph0ne"),
 (1, "Hi, I am from support team. Your electricity will be cut tonight. Transfer Rs 1,200 on UPI immediately to avoid disconnection."),
 (1, "Legal action will be taken against you. Pay the pending penalty now using gift cards."),
 (1, "Earn Rs 5000 daily from home, just deposit Rs 500 to start. Reply YES."),  # tricky: few signals
 # normal
 (0, "Hey, are we still meeting at 6 for the project discussion?"),
 (0, "Your OTP for login is 482913. Do not share it with anyone. - YourBank"),  # tricky: real OTP notice
 (0, "Reminder: your electricity bill of Rs 842 is due on 12 Nov. Pay via the official app."),
 (0, "Amma: please pay the school fee today, I will send you the amount tonight."),  # tricky: money + urgency words
 (0, "Congratulations on your results! Proud of you."),  # tricky: 'congratulations'
 (0, "Your Amazon order has shipped and will arrive Friday. Track it in the Amazon app."),
 (0, "Lunch at 1? I can transfer you my share for the pizza."),
 (0, "Report submission is due within 2 hours, please upload it on the portal."),
 (0, "Your package was delivered to the front desk at 3:40 PM."),
 (0, "Meeting moved to 4 PM. Link: https://meet.example.com/abc"),
]
