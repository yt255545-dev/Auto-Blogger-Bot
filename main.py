import smtplib
from email.message import EmailMessage
import os
import requests

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
    
    # আপনার দেওয়া মডেলগুলো ফ্রি ট্যাগসহ এখানে দেওয়া হলো
    data = {
        "model": "google/gemma-2-27b-it:free", 
        "messages": [{"role": "user", "content": "Write a professional educational article about Finance/Investment in English. Include an emotional hook, title (h1), and clear solution. Use HTML tags only."}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    # যদি প্রথম মডেলে এরর হয়, তবে দ্বিতীয় মডেলটি ট্রাই করবে
    if response.status_code != 200:
        data["model"] = "google/gemma-2-9b-it:free"
        response = requests.post(url, headers=headers, json=data)
        
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
        
    result = response.json()
    return result['choices'][0]['message']['content']

html_content = generate_ai_content()
msg = EmailMessage()
msg['Subject'] = "New Finance Strategy"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(html_content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_user, email_pass)
    smtp.send_message(msg)
    
