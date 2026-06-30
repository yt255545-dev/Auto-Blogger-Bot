import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import requests
import random
import time

# কনফিগারেশন
sender_email = "djr00397@gmail.com"
recipient_email = "yt255545.finance1@blogger.com"
email_pass = os.environ.get("EMAIL_PASS") # অবশ্যই অ্যাপ পাসওয়ার্ড হতে হবে

def send_to_blogger(content, title):
    # মেইল অবজেক্ট তৈরি
    msg = MIMEMultipart()
    msg['Subject'] = title
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # ব্লগার শুধু খুব সাধারণ HTML পছন্দ করে
    # সরাসরি ইমেইল বডিতে কোনো এক্সটার্নাল স্টাইল বা স্ক্রিপ্ট রাখা যাবে না
    body = f"<div>{content}</div>"
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, email_pass)
            smtp.send_message(msg)
            print("Successfully sent to Blogger!")
    except Exception as e:
        print(f"Error: {e}")

# উদাহরণস্বরূপ ব্যবহার
title = "Financial Tips 2026 - " + str(random.randint(100, 999))
content = """
<h2>Understanding Finance</h2>
<p>This is a simple automated post test.</p>
<ul>
    <li>Save money</li>
    <li>Invest wisely</li>
</ul>
<p>Visit our site for more.</p>
"""

# ফাংশন কল
send_to_blogger(content, title)
