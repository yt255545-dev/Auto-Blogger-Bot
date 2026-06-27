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

# ক্যাটাগরি সিরিয়াল মেইনটেইন (১০০% কাজ করবে)
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
    
    # এআই-কে নির্দেশ দেওয়া হয়েছে যেন কোনো স্টার, হ্যাশ বা কোড ব্লক না দেয়
    prompt = f"Write a professional SEO financial blog post about {category}. Structure: <h1>Title</h1>, <p>Meta Description</p>, <h2>Intro</h2>, <h2>Quick Answer</h2>, <h2>Steps</h2>, <h2>Pros & Cons</h2>, <h2>Mistakes</h2>, <h2>FAQ</h2>, <h2>Conclusion</h2>. DO NOT use markdown, asterisks, hashes, or code blocks. Start with <img src='{img}' style='width:100%; border-radius:10px;'>. Pure HTML text only."
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, timeout=40).json()
    
    raw = response['choices'][0]['message']['content']
    
    # সব ধরণের ভুল চিহ্ন জোর করে মুছে ফেলা (রিজেক্ট বাঁচানোর মূল চাবিকাঠি)
    clean = raw.replace("```html", "").replace("```", "").replace("**", "").replace("*", "").replace("#", "").strip()
    return clean

# পোস্ট তৈরি ও পাঠানো
content = generate_content(cat)
msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
