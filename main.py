import smtplib
from email.message import EmailMessage
import os
import requests
import random

email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance11@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    # এবার প্রম্পটটি এমনভাবে লিখেছি যেন সে কোনো স্টার ব্যবহার না করে এবং পরিষ্কার HTML দেয়
    prompt = f"""You are a professional Financial Blogger. Write an SEO-optimized article about '{cat}'.
    
    CRITICAL INSTRUCTIONS:
    1. DO NOT use asterisks (*), hashtags, or markdown formatting. Use HTML tags only (<h1>, <h2>, <p>, <ul>, <li>).
    2. Start with: <img src="https://source.unsplash.com/1200x600/?{cat.replace(' ', '+')}" alt="{cat}" style="width:100%; border-radius:10px;">
    3. Structure: 
       <h2>Introduction</h2><p>...</p>
       <h2>Problem Statement</h2><p>...</p>
       <h2>How It Works</h2><ul><li>...</li></ul>
       <h2>Key Benefits</h2><ul><li>...</li></ul>
       <h2>Expert Tips</h2><p>...</p>
       <h2>FAQ</h2><p>...</p>
    4. Ads: Insert '<div style="background:#f4f4f4; padding:20px; text-align:center;">AD SPACE</div>' after every two sections.
    5. No formatting symbols: Clean, simple, professional text only.
    6. Tone: Authoritative yet simple for common people."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"Complete Guide to {cat}"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
