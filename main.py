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
    
    # এসইও এবং রিডেবিলিটি প্রম্পট
    prompt = f"""You are a professional SEO expert and financial blogger. Write an 800+ word, engaging, human-like blog post about '{cat}'.
    
    Guidelines:
    1. Title: Use a 'Click-Worthy' title (e.g., "7 Secrets of...").
    2. Hook & Intro: Start with a personal hook or a real-life scenario. Keep paragraphs short (max 3-4 lines).
    3. Formatting: Use H2/H3 tags for headings. Use bullet points for tips/steps.
    4. Image: Add <img src="https://source.unsplash.com/800x400/?{cat.replace(' ', '+')}" alt="{cat}" style="width:100%; border-radius:10px;"> after the title.
    5. Value: Provide expert tips, do's/don'ts, and personal advice (not academic text).
    6. SEO: Include a Meta-description at the top. Use related keywords naturally.
    7. Ad-Ready: Insert '<div class="ad-block" style="text-align:center; margin:20px 0; background:#f9f9f9; padding:15px; border:1px dashed #ccc;">YOUR AD HERE</div>' after every 3 paragraphs.
    8. Interactive: Add a "Read More" button at the end: <a href="https://yt255545.blogspot.com/" style="padding:12px 25px; background:#ff4500; color:#fff; border-radius:5px; text-decoration:none;">Explore More Finance Tips</a>
    9. Tone: Conversational, simple, and expert. NO ASTERISKS (*) or Markdown symbols. Return valid HTML only."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# ক্যাটাগরি এবং পোস্ট
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"{cat} Guide: Everything You Need to Know"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
