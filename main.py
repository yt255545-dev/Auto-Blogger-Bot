import smtplib
from email.message import EmailMessage
import os
import requests

# গিটহাব সিক্রেট থেকে ডাটা নেওয়া
email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# ক্যাটাগরি সিরিয়াল মেইনটেইন করা
run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 0))
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = CATEGORIES[run_number % len(CATEGORIES)]

def get_image(query):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"[https://api.pexels.com/v1/search?query=](https://api.pexels.com/v1/search?query=){query}&per_page=1"
        response = requests.get(url, headers=headers, timeout=10).json()
        return response['photos'][0]['src']['large']
    except:
        return "[https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg](https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg)"

def generate_content(category):
    image_url = get_image(category.replace(" ", "+"))
    url = "[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"Write a professional, SEO-friendly finance article about {category}. Use clean HTML only: <h1>, <h2>, <p>, <ul>, <li>. No markdown, no asterisks, no hashes. Start with <img src='{image_url}' width='100%'>. Include Introduction, TL;DR, Steps, Pros/Cons, FAQs, and Conclusion."
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, timeout=30)
    raw_content = response.json()['choices'][0]['message']['content']
    
    # সব ধরণের ভুল চিহ্ন জোর করে মুছে ফেলা (ব্লগার রিজেক্ট থেকে বাঁচতে)
    clean_content = raw_content.replace("```html", "").replace("```", "").replace("**", "").replace("*", "").replace("#", "").strip()
    return clean_content

content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"{cat} Guide 2026"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
msg['Subject'] = f"Complete Guide to {cat} (2026 Edition)"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)
    print("Success! 100% SEO Post published to Blogger.")
except Exception as e:
    print(f"Failed to send email: {e}")
    
