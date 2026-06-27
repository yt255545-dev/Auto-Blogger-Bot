import smtplib
from email.message import EmailMessage
import os
import requests

# গিটহাব সিক্রেট থেকে ডাটা নেওয়া
sender_email = os.environ.get("EMAIL_USER")
app_password = os.environ.get("EMAIL_PASS")
blogger_email = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = CATEGORIES[(run_number - 1) % len(CATEGORIES)]

def get_image(query):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        data = requests.get(url, headers=headers, timeout=10).json()
        return data['photos'][0]['src']['large']
    except:
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

def generate_content(category):
    img = get_image(category)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"Write an expert 800+ word financial guide about '{category}'. Use HTML (<h1>, <h2>, <p>, <ul>, <li>, <table>). No markdown, no stars, no hashes. Start with <img src='{img}' style='width:100%; border-radius:10px;'>. Include SEO title, Meta Description, Steps, Pros/Cons, FAQ, and Keywords."
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, timeout=60).json()
    raw = response['choices'][0]['message']['content']
    return raw.replace("```html", "").replace("```", "").replace("**", "").replace("*", "").replace("#", "").strip()

# পোস্ট পাঠানো
content = generate_content(cat)
msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = sender_email
msg['To'] = blogger_email
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)
