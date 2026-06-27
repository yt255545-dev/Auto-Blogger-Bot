import smtplib
from email.message import EmailMessage
import os
import requests

# গিটহাব সিক্রেট থেকে তথ্য লোড করা
sender = os.environ.get("EMAIL_USER")
password = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# ক্যাটাগরি সিরিয়াল (প্রতি রান-এ একটি)
run_num = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
cats = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = cats[(run_num - 1) % len(cats)]

def generate_post(cat):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    # কঠোর নির্দেশিত প্রম্পট
    prompt = f"""Write an SEO-expert guide about '{cat}'. Output ONLY pure HTML tags (<h1>, <h2>, <p>, <ul>, <li>, <table>). No markdown, no stars, no hashes, no introduction text. Start directly with <h1>{cat} Guide 2026</h1>. Add 2-3 paragraphs for intro, a table for pros/cons, and 3 FAQs."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data).json()
    content = response['choices'][0]['message']['content']
    
    # সব ক্ষতিকর চিহ্ন মুছে ফেলা
    return content.replace("```html", "").replace("```", "").replace("**", "").replace("*", "").replace("#", "").strip()

# ইমেইল গঠন ও পাঠানো
msg = EmailMessage()
msg['Subject'] = f"{cat} Expert Guide 2026"
msg['From'] = sender
msg['To'] = recipient
msg.set_content(generate_post(cat), subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender, password)
    smtp.send_message(msg)
