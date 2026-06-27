import smtplib
from email.message import EmailMessage
import os
import requests

email_user = "Yt255545@gmail.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# ক্যাটাগরি লিস্ট (একটির পর একটি চলবে)
CATEGORIES = [
    "Credit Cards", "Loans", "Banking", "Investing", 
    "Insurance", "Taxes", "Personal Finance"
]

def get_next_category():
    # গিটহাব অ্যাকশন রান করার সময় একটি ফাইল থেকে শেষ ক্যাটাগরি চেক করবে
    filename = "last_index.txt"
    if not os.path.exists(filename):
        index = 0
    else:
        with open(filename, "r") as f:
            index = int(f.read().strip())
    
    current_cat = CATEGORIES[index]
    
    # ইনডেক্স আপডেট করা
    next_index = (index + 1) % len(CATEGORIES)
    with open(filename, "w") as f:
        f.write(str(next_index))
        
    return current_cat

def generate_ai_content(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yt255545-dev/Auto-Blogger-Bot"
    }
    
    # প্রতিটি পোস্ট ইউনিক করার জন্য প্রম্পট
    prompt = f"""Write a unique, professional, high-quality, SEO-optimized blog post in English about: {cat}.
    Requirements:
    1. Catchy H1 Title.
    2. Use H2 and H3 tags.
    3. Include a relevant Unsplash image URL at the top.
    4. Insert '' after intro, middle, and end.
    5. Write 800+ words, unique content, no repetition.
    6. Include FAQ section.
    7. Use HTML tags only."""

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")
    return response.json()['choices'][0]['message']['content']

# মেইন লজিক
cat = get_next_category()
html_content = generate_ai_content(cat)

msg = EmailMessage()
msg['Subject'] = f"{cat}: Latest Update"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(html_content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
