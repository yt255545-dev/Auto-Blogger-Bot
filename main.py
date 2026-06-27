import smtplib
from email.message import EmailMessage
import os
import requests

# কনফিগারেশন
email_user = "yt255545.Finance1@blogger.com"
email_pass = os.environ.get("EMAIL_PASS")
recipient = "yt255545.Finance1@blogger.com"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

def generate_ai_content():
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/yt255545-dev/Auto-Blogger-Bot"
    }
    
    # আপনার কাঙ্ক্ষিত মডেলটি এখানে বসিয়েছি
    prompt = "Write a professional educational article about Finance/Investment in English. Include an emotional hook and solution. Use HTML tags (h1 for title, p for body)."
    
    data = {
        "model": "google/gemma-2-27b-it:free", 
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
        
    result = response.json()
    return result['choices'][0]['message']['content']

# কন্টেন্ট পাঠানো
html_content = generate_ai_content()

msg = EmailMessage()
msg['Subject'] = "Finance Strategy Update"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(html_content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
