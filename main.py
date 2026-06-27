import smtplib
from email.message import EmailMessage
import os
import requests
import random

email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    # এবার টেবিল বা স্টাইল ছাড়াই একদম সিম্পল স্ট্রাকচার দিচ্ছি
    prompt = f"""Write a simple, clean blog post about '{cat}'.
    Rules:
    1. Use simple HTML only: <h1>, <h2>, <p>, <ul>, <li>.
    2. NO <table> tags.
    3. NO <div> or complex style tags.
    4. NO Image tags if they cause issues.
    5. Clean, high-quality information only."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"Guide: {cat}"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
