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
    
    # আপনার দেওয়া স্ট্রাকচার অনুযায়ী প্রম্পট
    prompt = f"""You are a top-tier SEO Finance Expert. Write an exhaustive, professional blog post in English about '{cat}'. 
    Strictly follow this structure:
    
    1. Title: Create an SEO-optimized H1 Title.
    2. Image: Use this exact HTML tag at the top: <img src="https://images.unsplash.com/photo-1554224155-8d04cb27cd6c?w=1200" alt="{cat} finance guide" style="width:100%; height:auto;">
    3. Content Structure: Strictly include: Introduction, Problem Statement, Definition, How It Works, Step-by-Step Guide, Pros & Cons, Common Mistakes, Expert Tips, FAQs, and Conclusion.
    4. Formatting: Use H2 for major headings, H3 for sub-points. Use clean Bullet Points.
    5. Ads: Insert '<div class="adsense-block"> [AD_SPACE] </div>' after the Intro, middle, and end.
    6. SEO: Add a Meta Description in italics at the start.
    7. Professionalism: Write in a helpful, conversational, and authoritative tone. No asterisks (*). No markdown. Return valid HTML only.
    8. CTA: Add a button at the end: <a href="https://yt255545.blogspot.com/" style="padding:15px; background:blue; color:white; border-radius:5px;">Read More Finance Tips</a>"""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"Guide: {cat} - Expert Financial Advice for 2026"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
