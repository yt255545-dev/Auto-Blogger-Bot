import smtplib
from email.message import EmailMessage
import os
import requests

# আপনার সিক্রেটগুলো গিটহাব থেকে সরাসরি নিচ্ছে
email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# ক্যাটাগরি সিরিয়াল মেইনটেইন
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
    
    # এসইও এবং স্ট্রাকচারড কন্টেন্ট প্রম্পট
    prompt = f"""Write an authoritative financial blog post about {category}. 
    STRICT FORMAT: Use ONLY <h1>, <h2>, <p>, <ul>, <li> tags. No asterisks, no hashes, no markdown, no code blocks. 
    Start with: <img src='{img}' style='width:100%;'>
    Follow: SEO Title, Meta Description (in italic), Intro, Quick Answer, 3-Step Guide, Pros & Cons List, 2 Common Mistakes, FAQ section, Conclusion.
    Tone: Professional, simple English, highly readable."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, timeout=40).json()
    
    raw = response['choices'][0]['message']['content']
    # রিজেক্ট বাঁচানোর জন্য সকল মার্কডাউন ও স্টার চিহ্ন রিমুভ করছি
    clean = raw.replace("```", "").replace("**", "").replace("#", "").replace("html", "").strip()
    return clean

# ইমেইল প্রস্তুতি
content = generate_content(cat)
msg = EmailMessage()
msg['Subject'] = f"Complete Guide to {cat} (2026 Edition)"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

# ইমেইল পাঠানো
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
