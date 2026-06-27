import smtplib
from email.message import EmailMessage
import os
import requests
import random

email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY") # এটি নতুন সিক্রেট হিসেবে গিটহাবে যোগ করুন

def get_pexels_image(query):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        response = requests.get(url, headers=headers).json()
        return response['photos'][0]['src']['large']
    except:
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

def generate_content(cat):
    image_url = get_pexels_image(cat.replace(" ", "+"))
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write an SEO-expert financial blog post about '{cat}'.
    Follow this structure strictly using HTML tags only:
    
    <h1>[SEO Catchy Title]</h1>
    <img src="{image_url}" alt="{cat}" width="100%" style="border-radius:10px;">
    
    <h2>Introduction</h2><p>...</p>
    <h2>What is {cat}?</h2><p>...</p>
    <h2>Step-by-Step Guide</h2><ol><li>...</li></ol>
    <h2>Pros & Cons</h2><table><tr><th>Pros</th><th>Cons</th></tr><tr><td>...</td><td>...</td></tr></table>
    <h2>FAQs</h2><h3>Q: ...</h3><p>A: ...</p>
    
    <div style="background:#f4f4f4; padding:15px; border-radius:5px;">AD SPACE</div>
    
    <a href="https://yt255545.blogspot.com/" style="padding:10px; background:blue; color:white;">Read More</a>
    
    NO asterisks (*), NO markdown. Clean HTML only."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"Guide: {cat} (2026 Edition)"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
