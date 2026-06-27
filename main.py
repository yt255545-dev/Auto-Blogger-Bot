import smtplib
from email.message import EmailMessage
import os
import requests
import random

# ১. সিক্রেট লোড করা
sender = os.environ.get("EMAIL_USER")
password = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# ২. সিরিয়াল অনুযায়ী ক্যাটাগরি নির্ধারণ
run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = CATEGORIES[(run_number - 1) % len(CATEGORIES)]

def generate_content(cat):
    # ৩. ছবি নেওয়া
    img_url = "[https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg](https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg)"
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        res = requests.get(f"[https://api.pexels.com/v1/search?query=](https://api.pexels.com/v1/search?query=){cat}&per_page=1", headers=headers).json()
        img_url = res['photos'][0]['src']['large']
    except: pass
    
    # ৪. এআই কন্টেন্ট জেনারেশন
    url = "[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Write an SEO-expert guide about {cat}. Use ONLY pure HTML tags like <h1>, <h2>, <p>, <ul>, <li>. No markdown, no asterisks, no hashes, no code blocks. Start with <img src='{img_url}' width='100%'>. Include Intro, TL;DR, Steps, Pros/Cons, FAQ, Conclusion. Be professional and 100% SEO optimized."
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data).json()
    content = response['choices'][0]['message']['content']
    
    # ৫. ক্লিন করা
    return content.replace("```html", "").replace("```", "").replace("**", "").replace("*", "").replace("#", "").strip()

# ৬. ইমেইল পাঠানো
msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = sender
msg['To'] = recipient
msg.set_content(generate_content(cat), subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)
    
