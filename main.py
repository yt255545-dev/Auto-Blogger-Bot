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
    
    # আপনার দেওয়া ২০টি পয়েন্টসহ প্রম্পট
    prompt = f"""Write an exhaustive, high-authority blog post about '{cat}'. Use pure HTML only. NO markdown, NO asterisks (*).
    
    STRUCTURE REQUIRED:
    1. SEO Title (H1) & Meta Description (in italic <p>).
    2. Table of Contents (Use a simple <ul> list with links).
    3. Quick Answer (TL;DR) in a highlighted box.
    4. Definition, Types, and Step-by-Step Guide (Use <ol>).
    5. Real-Life Example & Comparison Table (Use <table>).
    6. Pros & Cons (Use <table> or <ul>).
    7. Fees, Risks, Common Mistakes, Best Practices.
    8. Latest Updates (2026), Key Takeaways, and Conclusion.
    9. Call to Action: Add a button to explore more.
    10. References: Mention 'Sources: Trusted Finance Data 2026'.
    
    - Image: Add <img src="https://source.unsplash.com/1200x600/?{cat.replace(' ', '+')}" style="width:100%; border-radius:10px;">
    - Ads: Insert <div style="background:#f9f9f9; padding:20px; text-align:center;">AD SPACE</div> every 3 sections.
    - Style: Professional, authoritative, clean, and mobile-friendly."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"Comprehensive Guide: {cat} (2026 Update)"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
