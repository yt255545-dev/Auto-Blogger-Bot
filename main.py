import smtplib
import os
from email.message import EmailMessage
import requests
from dotenv import load_dotenv

# .env ফাইল থেকে তথ্য লোড করা
load_dotenv()

# সরাসরি কোড থেকে নয়, বরং এনভায়রনমেন্ট থেকে তথ্য নেওয়া
sender_email = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
recipient_email = "yt255545.finance1@blogger.com" # আপনার ব্লগার আইডি

# অন্যান্য API কী
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# ... (আপনার আগের ফাংশনগুলো যেমন get_pexels_image এবং generate_content এখানে রাখুন) ...

def send_email_post(content, subject):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Message-ID'] = f"<{os.urandom(8).hex()}@your-domain.com>" # অ্যান্টি-স্প্যাম হেডার
    msg.set_content(content, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, email_pass)
            smtp.send_message(msg)
            print("পোস্ট সফলভাবে পাঠানো হয়েছে!")
    except Exception as e:
        print(f"ইমেইল পাঠানোর সময় সমস্যা হয়েছে: {e}")

# মেইন লজিক
content = generate_content(cat)
send_email_post(content, f"{cat} Expert Guide 2026")
        
