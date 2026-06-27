import smtplib
from email.message import EmailMessage
import os
import requests
import random

# ইউজার সেটিংস
email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# ১. ক্যাটাগরি লিস্ট
CATEGORIES = [
    "Credit Cards", "Loans", "Banking", "Investing", 
    "Insurance", "Taxes", "Personal Finance"
]

def get_category():
    # গিটহাব অ্যাকশন প্রতিবার রান করার সময় এখান থেকে একটি ক্যাটাগরি বেছে নেবে
    return random.choice(CATEGORIES)

def generate_ai_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yt255545-dev/Auto-Blogger-Bot"
    }
    
    # ২. এসইও এবং অ্যাড-ফ্রেন্ডলি প্রম্পট (সম্পূর্ণ অটোমেশন)
    prompt = f"""Write a unique, professional, high-quality, SEO-optimized blog post in English about: {cat}.
    Requirements:
    - Target Category: {cat}
    - Title: Create a catchy, SEO-friendly H1 title.
    - Structure: Use proper H2 and H3 tags.
    - Images: Include one relevant Unsplash image URL at the top.
    - Monetization: Insert '' after the introduction, middle, and before the conclusion.
    - Length: Write 800+ words of unique, informative content.
    - SEO: Include an FAQ section at the end and naturally use keywords related to {cat}.
    - Format: Use HTML tags ONLY. Do not use Markdown code blocks."""

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")
    return response.json()['choices'][0]['message']['content']

# মেইন লজিক
category = get_category()
html_content = generate_ai_content(category)

# ইমেইল সেন্ডিং
msg = EmailMessage()
msg['Subject'] = f"{category}: {random.randint(100, 999)} - New Update"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(html_content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
