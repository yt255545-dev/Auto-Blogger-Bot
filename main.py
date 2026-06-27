import smtplib
from email.message import EmailMessage
import os
import requests
import random

email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_ai_content():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yt255545-dev/Auto-Blogger-Bot"
    }
    
    # উন্নত SEO এবং অ্যাড-ফ্রেন্ডলি প্রম্পট
    topics = ["Passive Income Strategies", "Best Investment Trends 2026", "Stock Market for Beginners", "Cryptocurrency Tips", "Budgeting Hacks"]
    selected_topic = random.choice(topics)
    
    prompt = f"""Write a professional, high-quality, SEO-optimized blog post in English about: {selected_topic}.
    Requirements:
    1. Catchy H1 Title.
    2. Use H2 and H3 tags for structure.
    3. Include a high-quality relevant Unsplash image URL at the top.
    4. Insert '' tag after the introduction, middle, and before the conclusion.
    5. Write 600+ words with engaging content.
    6. Include a clear 'Conclusion' and FAQ section for SEO.
    7. Use HTML tags only."""

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result['choices'][0]['message']['content']

html_content = generate_ai_content()
msg = EmailMessage()
msg['Subject'] = "Finance Insight"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(html_content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)

