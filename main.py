import smtplib
from email.message import EmailMessage
import os
import requests

# ১. আপনার আসল জিমেইল (যেটার App Password গিটহাবে দেওয়া আছে)
email_user = "Yt255545@gmail.com"

# ২. গিটহাব সিক্রেট থেকে আপনার App Password নেবে
email_pass = os.environ.get("EMAIL_PASS")

# ৩. আপনার ব্লগারের সিক্রেট ইমেইল (যেখানে ইমেইল গেলে ব্লগারে পোস্ট হবে)
recipient = "yt255545.Finance1@blogger.com"

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_ai_content():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yt255545-dev/Auto-Blogger-Bot"
    }
    
    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": "Write a professional educational article about Finance/Investment in English. Include an emotional hook, title (h1), and clear solution. Use HTML tags only."}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
        
    result = response.json()
    return result['choices'][0]['message']['content']

# AI দিয়ে কন্টেন্ট জেনারেট করা হচ্ছে
html_content = generate_ai_content()

# ইমেইল সেটআপ করা হচ্ছে
msg = EmailMessage()
msg['Subject'] = "New Finance Strategy"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(html_content, subtype='html')

# গুগলের সার্ভারে লগইন করে ব্লগারে ইমেইল পাঠানো হচ্ছে
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
