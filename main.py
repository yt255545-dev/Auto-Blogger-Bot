import smtplib
from email.message import EmailMessage
import os
import requests
import random

# সিক্রেট থেকে ডাটা নেওয়া
email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

def get_pexels_image(query):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        response = requests.get(url, headers=headers).json()
        return response['photos'][0]['src']['large']
    except:
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

def generate_content(cat):
    image_url = get_pexels_image(cat.replace(" ", "+"))
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    # এখানে প্রম্পটটি কন্টেন্ট এবং এসইও স্ট্রাকচারের ওপর গুরুত্ব দিয়েছে
    prompt = f"""Write an authoritative, SEO-optimized financial guide about '{cat}'. 
    Use semantic HTML only. NO markdown, NO asterisks, NO 'AD SPACE' text.
    
    STRUCTURE:
    <h1>{cat} Guide 2026: Everything You Need to Know</h1>
    <img src="{image_url}" alt="{cat} finance" width="100%">
    
    <p><em>Meta Description: A complete guide on {cat} covering types, risks, benefits, and expert tips for 2026.</em></p>
    
    <h2>Introduction</h2>
    <p>Hook the reader with a scenario, then define {cat}.</p>
    
    <h2>Quick Answer (TL;DR)</h2>
    <p>Provide a 2-3 sentence summary.</p>
    
    <h2>What is {cat} and How It Works?</h2>
    <p>Expert explanation...</p>
    
    <h2>Key Types of {cat}</h2>
    <ul><li>Type 1</li><li>Type 2</li></ul>
    
    <h2>Step-by-Step Guide</h2>
    <ol><li>Step 1</li><li>Step 2</li></ol>
    
    <h2>Pros and Cons</h2>
    <table><tr><th>Benefits</th><th>Drawbacks</th></tr><tr><td>...</td><td>...</td></tr></table>
    
    <h2>Common Mistakes and Best Practices</h2>
    <p>Expert advice...</p>
    
    <h2>FAQs</h2>
    <h3>What is the biggest risk in {cat}?</h3>
    <p>Detailed answer...</p>
    
    <h2>Latest Updates 2026 and Conclusion</h2>
    <p>Summary and final recommendation.</p>
    
    <p><a href="https://yt255545.blogspot.com/">Explore More Financial Tips</a></p>
    """
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
