import smtplib
from email.message import EmailMessage
import os
import requests
import random

# সিক্রেট থেকে ডাটা নেওয়া
email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

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
    
    # এবার একদম সিম্পল HTML ব্যবহার করেছি যাতে ব্লগার রিজেক্ট না করে
    prompt = f"""Write an SEO-expert financial guide about '{cat}'.
    Rules:
    1. Use simple HTML: <h1>, <h2>, <p>, <ul>, <li>.
    2. No tables, no divs, no complex CSS.
    3. Include: Title, Meta Description (in italic), Intro, Steps (numbered list), Pros & Cons (bullet points), Common Mistakes, Expert Tips, FAQs.
    4. Start with: <img src="{image_url}" alt="{cat}" width="100%">
    5. Clean text only. No markdown, no asterisks, no special characters.
    6. Tone: Authoritative, simple, and professional."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# পোস্ট জেনারেশন
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
