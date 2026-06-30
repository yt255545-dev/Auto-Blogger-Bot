import smtplib
from email.message import EmailMessage
import os
import requests
import random
import subprocess

# --- কনফিগারেশন ---
sender_email = "djr00397@gmail.com"
recipient_email = "yt255545.Finance1@blogger.com"
email_pass = os.environ.get("EMAIL_PASS")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")
HISTORY_FILE = "used_images.txt"

# --- হিস্ট্রি ট্র্যাকার ---
def get_used_images():
    if not os.path.exists(HISTORY_FILE): return set()
    with open(HISTORY_FILE, "r") as f: return set(line.strip() for line in f)

def save_used_image(image_url):
    with open(HISTORY_FILE, "a") as f: f.write(image_url + "\n")

# --- ছবি সংগ্রহের ফাংশন ---
def get_pexels_image(query):
    used_images = get_used_images()
    headers = {"Authorization": PEXELS_API_KEY}
    # র‍্যান্ডম পেজ ও ইউনিক ছবির জন্য চেষ্টা
    for _ in range(3):
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=15&page={random.randint(1, 20)}"
        try:
            response = requests.get(url, headers=headers).json()
            if 'photos' in response:
                photos = response['photos']
                random.shuffle(photos)
                for photo in photos:
                    img_url = photo['src']['large']
                    if img_url not in used_images:
                        save_used_image(img_url)
                        return img_url
        except: continue
    return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

# --- কন্টেন্ট জেনারেশন (হিউম্যান-লাইক ও এসইও অপ্টিমাইজড) ---
def generate_content(cat):
    image_url = get_pexels_image(cat)
    image_html = f'<img src="{image_url}" alt="{cat}" style="width:100%; border-radius:10px; margin-bottom:20px;">'
    
    prompt = f"""You are a senior financial expert writing for a professional finance blog in 2026. Write an authoritative, highly engaging, and 100% SEO-optimized post about '{cat}'.
    
    GUIDELINES:
    1. Title: Create a compelling H1 title.
    2. Meta Description: 150 characters in <p style="font-style:italic;">.
    3. Start with: {image_html}
    4. Structure: 
       - Introduction: Hook the reader, current 2026 landscape.
       - Evolution: Brief history (lessons from the past) vs. the future of '{cat}'.
       - Real-world example: A relatable scenario (e.g., 'Imagine you are...') to simplify complex ideas.
       - Pros & Cons: Use a clean <table>.
       - Common Mistakes, FAQ, Conclusion.
    5. Formatting: Use ONLY <h2>, <h3>, <p>, <ul>, <li>, <table>. No markdown.
    6. Ads: Insert <div style="margin:20px 0; text-align:center; background:#f9f9f9; padding:15px;">[AD_SPACE]</div> after Intro and after the Table.
    7. Tone: Human-written, professional, and empathetic.
    """
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "meta-llama/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    
    response = requests.post(url, headers=headers, json=data).json()
    content = response['choices'][0]['message']['content']
    return content.replace("```html", "").replace("```", "").strip()

# --- মেইন এক্সিকিউশন ---
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = CATEGORIES[int(os.environ.get("GITHUB_RUN_NUMBER", 1)) % len(CATEGORIES)]

content = generate_content(cat)
msg = EmailMessage()
msg['Subject'] = f"The Future of {cat}: Expert Insights for 2026"
msg['From'] = sender_email
msg['To'] = recipient_email
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, email_pass)
    smtp.send_message(msg)

# গিট আপডেট করার কমান্ড (গিটহাব অ্যাকশনে ব্যবহারের জন্য)
try:
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
    subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"])
    subprocess.run(["git", "add", HISTORY_FILE])
    subprocess.run(["git", "commit", "-m", "Update used images history"])
    subprocess.run(["git", "push"])
except: pass
                            
