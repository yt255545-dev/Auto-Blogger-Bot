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
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY") # এটি নতুন সিক্রেট হিসেবে যোগ করুন

def get_pixabay_image(query):
    try:
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=photo&per_page=3"
        response = requests.get(url).json()
        if response['hits']:
            return response['hits'][0]['largeImageURL']
    except:
        return "https://images.unsplash.com/photo-1554224155-8d04cb27cd6c"
    return "https://images.unsplash.com/photo-1554224155-8d04cb27cd6c"

def generate_content(cat):
    image_url = get_pixabay_image(cat.replace(" ", "+"))
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a high-authority SEO blog post about '{cat}'.
    Structure:
    1. Title: <h1>Title</h1>
    2. Image: <img src="{image_url}" alt="{cat}" width="100%">
    3. Content: Use <h2>, <p>, <ul>, <li> tags only. No markdown.
    4. Include: Definition, Step-by-Step guide, Pros/Cons (in <table>), and FAQ.
    5. Ad Space: [AD]
    6. Tone: Conversational, professional."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# পোস্ট জেনারেশন
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
    
