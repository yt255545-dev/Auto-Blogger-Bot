import smtplib
from email.message import EmailMessage
import os
import requests
import datetime

email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# ১. আপনার দেওয়া ৭টি ক্যাটাগরি
CATEGORIES = [
    "Credit Cards", "Loans", "Banking", "Investing", 
    "Insurance", "Taxes", "Personal Finance"
]

def get_current_category():
    # বর্তমান তারিখের ওপর ভিত্তি করে ক্যাটাগরি বেছে নেবে, তাই ক্যাটাগরি বদলাতেই থাকবে
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return CATEGORIES[day_of_year % len(CATEGORIES)]

def generate_ai_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yt255545-dev/Auto-Blogger-Bot"
    }
    
    # এসইও এবং অ্যাডস সহ প্রম্পট
    prompt = f"""Write a unique, professional, 800-word SEO-optimized blog post in English about: {cat}.
    Guidelines:
    1. Title: Create a catchy, SEO-friendly H1 title.
    2. Category: {cat}
    3. Images: Add a relevant Unsplash image URL at the very top.
    4. Ads: Insert '' after the introduction, middle, and end.
    5. SEO: Use H2/H3 headings, include an FAQ section, and naturally use keywords.
    6. Content: Unique, high-quality, and informative.
    7. Format: Return HTML tags ONLY. No markdown, no triple backticks."""

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
        
    return response.json()['choices'][0]['message']['content']

# পোস্ট জেনারেশন
cat = get_current_category()
html_content = generate_ai_content(cat)

# ইমেইল পাঠানো
msg = EmailMessage()
msg['Subject'] = f"{cat} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(html_content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
