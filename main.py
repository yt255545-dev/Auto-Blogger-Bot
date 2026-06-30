import smtplib
from email.message import EmailMessage
import os
import requests
import random

# কনফিগারেশন
sender_email = "djr00397@gmail.com"
recipient_email = "yt255545.finance1@blogger.com"

# এনভায়রনমেন্ট ভেরিয়েবল থেকে কি (Key) সংগ্রহ
email_pass = os.environ.get("EMAIL_PASS")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
cat = CATEGORIES[(run_number - 1) % len(CATEGORIES)]

def get_pexels_image(query):
    # র‍্যান্ডম ছবি পাওয়ার জন্য পেজ নম্বর র‍্যান্ডমাইজ করা হয়েছে
    page = random.randint(1, 10)
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=15&page={page}"
        response = requests.get(url, headers=headers).json()
        
        photos = response.get('photos', [])
        if photos:
            photo = random.choice(photos)
            return photo['src']['large']
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"
    except:
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

def generate_content(cat):
    image_url = get_pexels_image(cat)
    # ছবির সাইজ ছোট এবং সেন্টার করার জন্য CSS স্টাইল
    image_html = f'<div style="text-align:center;"><img src="{image_url}" alt="{cat}" style="max-width: 600px; width: 100%; height: auto; border-radius: 10px; margin-bottom: 20px;"></div>'
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a high-quality, 100% SEO-optimized financial blog post about '{cat}'.
    
    CRITICAL RULES:
    1. Start immediately with this image: {image_html}
    2. Write an SEO Title (<h1>) and Meta Description (in italic).
    3. Use only pure HTML tags (<h2>, <p>, <ul>, <li>). NO markdown symbols (*, #, `).
    4. Structure: Intro, How it works, Pros & Cons Table (use <table>), Common Mistakes, FAQ, and Conclusion.
    5. Ads: Insert <div style="margin:20px 0; text-align:center; background:#f9f9f9; padding:15px; border:1px solid #eee;">[AD_SPACE]</div> after every two sections.
    6. Tone: Authoritative, expert, and professional."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    
    # এরর হ্যান্ডলিং যোগ করা
    try:
        content = response.json()['choices'][0]['message']['content']
    except:
        content = "<h2>Sorry, content generation failed.</h2>"
    
    return content.replace("```html", "").replace("```", "").strip()

# ইমেইল পাঠানো
content = generate_content(cat)
msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = sender_email
msg['To'] = recipient_email
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, email_pass)
    smtp.send_message(msg)
        
