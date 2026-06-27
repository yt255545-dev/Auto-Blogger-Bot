import smtplib
from email.message import EmailMessage
import os
import requests
import random

# সেটিংস
email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# ক্যাটাগরি লিস্ট
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]

def get_and_update_category():
    # গিটহাবে 'category_index.txt' নামে একটি ফাইল ব্যবহার করছি যাতে সিরিয়াল বজায় থাকে
    filename = "category_index.txt"
    if not os.path.exists(filename):
        index = 0
    else:
        with open(filename, "r") as f:
            index = int(f.read().strip())
    
    cat = CATEGORIES[index % len(CATEGORIES)]
    
    # ইনডেক্স বাড়িয়ে ফাইল আপডেট করা
    with open(filename, "w") as f:
        f.write(str(index + 1))
    return cat

def generate_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a high-quality, 800+ words SEO-optimized blog post in English about: {cat}.
    - Title: Catchy H1.
    - Image: Add a relevant Unsplash image URL at the start.
    - Ads: Place '' after intro, middle, and end.
    - Structure: Use H2/H3, FAQ section, unique content.
    - Format: HTML only. No markdown formatting."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# পোস্ট জেনারেশন ও ইমেইল
cat = get_and_update_category()
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"{cat}: Exclusive Finance Tips"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
              
