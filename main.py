import smtplib
from email.message import EmailMessage
import os
import requests
import random
import time # টাইম ডিলে ব্যবহারের জন্য

# ... (অন্যান্য আগের কোডগুলো একই থাকবে)

def generate_content(cat):
    # ছবি সরাসরি ইমেইলের বডিতে না দিয়ে লিঙ্কের আকারে দেওয়া নিরাপদ
    image_url = get_pexels_image(cat)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    # প্রম্পটে পরিবর্তন: খুব বেশি জটিল HTML পরিহার করা হয়েছে
    prompt = f"""Write a professional financial blog post about '{cat}'.
    
    RULES:
    1. Do NOT include <img> tags or complex div layouts.
    2. Write an SEO Title and Meta Description clearly.
    3. Use simple HTML: <h2> for headers, <p> for paragraphs, <ul> for lists.
    4. Structure: Intro, How it works, Pros & Cons, Common Mistakes, Conclusion.
    5. At the end, add a text-based link to the image: Image: {image_url}
    6. Tone: Professional and natural, avoid "robotic" patterns."""
    
    # ... (বাকি কোড আগের মতো)

# ইমেইল পাঠানোর সময় কিছুটা র‍্যান্ডমাইজেশন ও ডিলে যোগ করা
def send_email_with_delay(content, cat):
    time.sleep(random.randint(60, 300)) # ১ থেকে ৫ মিনিটের একটি র‍্যান্ডম ডিলে
    
    msg = EmailMessage()
    # সাবজেক্ট লাইনকে ইউনিক করার জন্য টাইমস্ট্যাম্প যোগ করা
    msg['Subject'] = f"{cat} Analysis - {random.randint(1000, 9999)}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, email_pass)
        smtp.send_message(msg)

# ফাংশন কল
content = generate_content(cat)
send_email_with_delay(content, cat)
    
