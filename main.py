import smtplib
from email.message import EmailMessage
import os
import requests

# আপনার নতুন ইমেইল আইডি এবং ব্লগার পোস্টের ঠিকানা
sender_email = "djr00397@gmail.com"
recipient_email = "yt255545.finance1@blogger.com"

# সিক্রেট কি (গিটহাব সেটিংস থেকে আসবে)
email_pass = os.environ.get("EMAIL_PASS")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# ক্যাটাগরি সিরিয়াল
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
cat = CATEGORIES[(run_number - 1) % len(CATEGORIES)]

def get_pexels_image(query):
    # Pexels API ব্যবহার করে ছবি খোঁজা
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        response = requests.get(url, headers=headers).json()
        return response['photos'][0]['src']['large']
    except:
        # Pexels কাজ না করলে একটি ডিফল্ট ছবি
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

def generate_content(cat):
    image_url = get_pexels_image(cat)
    image_html = f'<img src="{image_url}" alt="{cat}" style="width:100%; border-radius:10px; margin-bottom:20px;">'
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a high-quality, 100% SEO-optimized financial blog post about '{cat}'.
    
    CRITICAL RULES:
    1. Start immediately with this image: {image_html}
    2. Write an SEO Title (<h1>) and Meta Description (in italic).
    3. Use only pure HTML tags (<h2>, <p>, <ul>, <li>). NO markdown symbols (*, #, ).
    4. Structure: Intro, How it works, Pros & Cons Table, Common Mistakes, FAQ, and Conclusion.
    5. Ads: Insert <div style="margin:20px 0; text-align:center; background:#f9f9f9; padding:15px;">[AD_SPACE]</div> after every two sections.
    6. Tone: Authoritative, expert, and professional."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    content = response.json()['choices'][0]['message']['content']
    
    return content.replace("``html", "").replace("`", "").strip()

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
