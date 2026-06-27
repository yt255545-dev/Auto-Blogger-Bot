import smtplib
from email.message import EmailMessage
import os
import requests
import random
import datetime

# সেটিংস
email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS") # গিটহাব সিক্রেটে অ্যাপ পাসওয়ার্ডটি রাখুন
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_content():
    # প্রতিবার রান করার সময় একটি র‍্যান্ডম ক্যাটাগরি বেছে নেবে
    categories = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
    cat = random.choice(categories)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Write an 800-word SEO-optimized blog post in English about {cat}.
    1. Include an H1 title.
    2. Use H2/H3 headings.
    3. Add a free Unsplash image URL at the start.
    4. Insert '' after intro, middle, and end.
    5. Include an FAQ section.
    6. Return HTML only. No Markdown."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content'], cat

content, cat = generate_content()
msg = EmailMessage()
msg['Subject'] = f"{cat} Update - {datetime.date.today()}"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
