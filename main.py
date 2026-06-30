import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests
import random
import time

# কনফিগারেশন (গিটহাব সিক্রেটস থেকে)
sender_email = "djr00397@gmail.com"
recipient_email = "yt255545.finance1@blogger.com"
email_pass = os.environ.get("EMAIL_PASS")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)

def generate_seo_content(category):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a unique, human-like, SEO-optimized blog post about '{category}'.
    1. Start with an engaging H1 title.
    2. Write a brief meta description in italics.
    3. Use H2 and H3 tags for structure.
    4. Keep paragraphs short (2-3 sentences).
    5. Tone: Informative, helpful, and expert.
    6. Ensure the content is structured for readability.
    7. NO CSS, NO JAVASCRIPT, NO DIVS. ONLY <p>, <h1>, <h2>, <h3>, <ul>, <li>.
    8. Use the emoji {category.split()[0]} in the title."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

def send_email(content):
    msg = MIMEMultipart()
    # টাইটেলটি প্রথম লাইন থেকে বের করার চেষ্টা
    lines = content.split('\n')
    title = lines[0].replace("#", "").replace("<h1>", "").replace("</h1>", "").strip()
    
    msg['Subject'] = title
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # পোস্ট বডিতে সরাসরি টেক্সট পাঠানো
    msg.attach(MIMEText(content, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, email_pass)
        smtp.send_message(msg)

# রান করা
content = generate_seo_content(cat)
send_email(content)
    
