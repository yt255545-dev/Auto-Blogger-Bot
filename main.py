import smtplib
from email.message import EmailMessage
import os
import requests

# গিটহাব সিক্রেট থেকে শুধুমাত্র প্রয়োজনীয় তথ্য নেওয়া হচ্ছে
recipient = os.environ.get("RECIPIENT_EMAIL") # ব্লগের পাবলিশিং ইমেইল
post_email = os.environ.get("RECIPIENT_EMAIL") # ব্লগের পাবলিশিং ইমেইলকেই সেন্ডার হিসেবে ব্যবহার করবে
email_pass = os.environ.get("EMAIL_PASS")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# ক্যাটাগরি সিরিয়াল (১০০% কাজ করবে)
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
    
    prompt = f"Write an expert 800+ word financial guide about '{category}'. Use only <h1>, <h2>, <p>, <ul>, <li>, <table>. No markdown, no stars, no hashes. Start with <img src='{img}' style='width:100%; border-radius:10px;'>. Include SEO title, Meta Description, Steps, Pros/Cons, FAQ, and Keywords at the end."
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, timeout=60).json()
    
    raw = response['choices'][0]['message']['content']
    return raw.replace("```html", "").replace("```", "").replace("**", "").replace("*", "").replace("#", "").strip()

# পোস্ট তৈরি ও পাঠানো
content = generate_content(cat)
msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = recipient  # এখানে আপনার সেই ব্লগার ইমেইল আইডিটিই ব্যবহার করা হয়েছে
msg['To'] = recipient    # পোস্ট যাওয়ার ঠিকানা
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(recipient, email_pass) # ব্লগার ইমেইল আইডি দিয়ে লগইন করবে
    smtp.send_message(msg)
    
