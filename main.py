import smtplib
from email.message import EmailMessage
import os
import requests
import random

# একদম ঠিক! সবকিছু এখন আপনার সেটআপ করা সিক্রেট (Secret) বাক্স থেকেই আসবে।
email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

def get_image(query):
    if not PEXELS_API_KEY:
        return f"https://source.unsplash.com/1200x600/?{query}"
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        response = requests.get(url, headers=headers, timeout=10).json()
        if response.get('photos'):
            return response['photos'][0]['src']['large']
    except Exception as e:
        print(f"Image Error: {e}")
    return f"https://source.unsplash.com/1200x600/?{query}"

def generate_content(cat):
    image_url = get_image(cat.replace(" ", "+"))
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"""Write a highly engaging, SEO-optimized finance blog post about '{cat}'.
    CRITICAL RULES:
    1. Output ONLY pure HTML. Do NOT wrap the response in ```html or ``` blocks.
    2. NO markdown, NO asterisks (*).
    
    REQUIRED STRUCTURE:
    <h1>{cat} Guide 2026: Expert Financial Strategies</h1>
    <img src="{image_url}" alt="{cat} Guide" style="width:100%; border-radius:8px;">
    
    <p><em>Meta Description: An essential and complete guide to {cat} for 2026. Learn the steps, benefits, risks, and expert tips to manage your finances better.</em></p>
    
    <h2>Introduction</h2>
    <p>[Write a catchy introduction]</p>
    
    <h2>Quick Answer (TL;DR)</h2>
    <p><strong>Summary:</strong> [1-2 sentences summarizing the topic]</p>
    
    <h2>How It Works</h2>
    <p>[Explain the concept clearly]</p>
    
    <h2>Step-by-Step Guide</h2>
    <ul><li>[Step 1]</li><li>[Step 2]</li><li>[Step 3]</li></ul>
    
    <h2>Pros & Cons</h2>
    <ul>
      <li><strong>Pros:</strong> [List 2 pros]</li>
      <li><strong>Cons:</strong> [List 2 cons]</li>
    </ul>
    
    <h2>Common Mistakes to Avoid</h2>
    <p>[Explain 2-3 mistakes]</p>
    
    <h2>FAQs</h2>
    <h3>What is the best way to start with {cat}?</h3>
    <p>[Answer]</p>
    
    <h2>Conclusion</h2>
    <p>[Final thoughts]</p>
    """
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, timeout=30)
    raw_content = response.json()['choices'][0]['message']['content']
    
    # এআই-এর ভুল ফরম্যাটিং ক্লিন করা
    clean_content = raw_content.replace("```html", "").replace("```", "").strip()
    return clean_content

print("Starting to generate content...")
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = random.choice(CATEGORIES)
content = generate_content(cat)
print("Content generated successfully! Sending to Blogger...")

msg = EmailMessage()
msg['Subject'] = f"Complete Guide to {cat} (2026 Edition)"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)
    print("Success! Post published to Blogger.")
except Exception as e:
    print(f"Failed to send email: {e}")
    
