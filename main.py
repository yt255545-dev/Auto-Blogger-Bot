import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests
import random

# কনফিগারেশন
SENDER_EMAIL = "djr00397@gmail.com"
RECIPIENT_EMAIL = "yt255545.finance1@blogger.com"
EMAIL_PASS = os.environ.get("EMAIL_PASS")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# ক্যাটাগরি তালিকা
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]

def get_next_category():
    # গিটহাব রান নাম্বারের উপর ভিত্তি করে ক্যাটাগরি সিলেক্ট হবে (প্রতিবার এক একটি করে)
    run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
    return CATEGORIES[(run_number - 1) % len(CATEGORIES)]

def generate_seo_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a professional, 100% unique, human-like SEO blog post about '{cat}'.
    Rules:
    1. Title: Create an engaging SEO-friendly H1 title including '{cat}'.
    2. Meta Description: Write a short, italicized description at the start.
    3. Use H2 and H3 tags to structure sections.
    4. Structure: Introduction, Detailed Tips, Common Mistakes, FAQ, Conclusion.
    5. No CSS, No Divs, No Scripts. Only HTML tags: <h1>, <h2>, <h3>, <p>, <ul>, <li>, <strong>, <em>.
    6. Ensure the tone is authoritative and helpful."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

def send_to_blogger(content):
    msg = MIMEMultipart()
    # টাইটেল বের করা
    title_line = content.split('\n')[0].replace("#", "").replace("<h1>", "").replace("</h1>", "").strip()
    msg['Subject'] = title_line
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    
    msg.attach(MIMEText(content, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, EMAIL_PASS)
        smtp.send_message(msg)

# মেইন লজিক
if __name__ == "__main__":
    category = get_next_category()
    print(f"Generating post for: {category}")
    post_content = generate_seo_content(category)
    send_to_blogger(post_content)
    print("Post successfully sent!")

