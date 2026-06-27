import smtplib
from email.message import EmailMessage
import os
import requests
import random

email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    # এসইও এবং মনিটাইজেশন ফ্রেন্ডলি প্রম্পট
    prompt = f"""Write an 800+ word professional, human-like SEO blog post about '{cat}'.
    IMPORTANT RULES:
    1. NO ASTERISKS (*) or Markdown symbols. Use clean HTML tags (<h1>, <h2>, <p>, <ul>).
    2. Start with an image: <img src="https://source.unsplash.com/800x400/?{cat.replace(' ', '+')}" alt="{cat}" style="width:100%; height:auto;">
    3. Use catchy H1 title. Use H2 for sub-headings.
    4. Ad Placement: Insert '<div style="background:#f4f4f4; padding:20px; text-align:center;">YOUR AD HERE</div>' after intro, middle, and end.
    5. SEO: Include an FAQ section at the end.
    6. Category Button: Add this HTML at the very end: <a href="https://yt255545.blogspot.com/search/label/{cat.replace(' ', '%20')}" style="padding:10px 20px; background:blue; color:white; text-decoration:none;">View More {cat} Articles</a>
    7. Tone: Informative, helpful, and professional."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# ক্যাটাগরি লজিক
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"{cat}: Expert Guide"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
