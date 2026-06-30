import smtplib
from email.message import EmailMessage
import os
import requests

# এনভায়রনমেন্ট ভেরিয়েবল থেকে কীগুলো নিচ্ছে
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

sender_email = "djr00397@gmail.com"
recipient_email = "yt255545.Finance1@blogger.com"

# --- Gemini Imagen API ব্যবহার করে ছবি তৈরি ---
def generate_image_with_gemini(query):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={GEMINI_API_KEY}"
    
    prompt = f"A professional, high-quality, photorealistic financial blog header image about {query}. 16:9 aspect ratio, 1200x675 resolution, web-ready."
    
    payload = {
        "instances": [{"prompt": prompt}],
        "params": {
            "aspectRatio": "16:9",
            "sampleCount": 1,
            "outputMimeType": "image/webp"
        }
    }
    
    try:
        response = requests.post(url, json=payload).json()
        img_data = response['predictions'][0]['bytesBase64Encoded']
        return f"data:image/webp;base64,{img_data}"
    except Exception as e:
        print(f"Image API Error: {e}")
        return "https://via.placeholder.com/1200x675.png?text=Financial+Blog+Image"

# --- কন্টেন্ট জেনারেশন ---
def generate_content(cat):
    image_src = generate_image_with_gemini(cat)
    image_html = f'<img src="{image_src}" alt="{cat}" style="width:100%; max-width:1200px; height:auto; border-radius:10px; margin-bottom:20px;">'
    
    prompt = f"""Write an SEO-optimized blog post about '{cat}' for 2026.
    Follow: H1 title, Meta description, Intro (2026 context), Lessons from past vs Future, Real-world examples, Pros/Cons Table.
    Use HTML tags only. Insert <div style="margin:20px 0; text-align:center; background:#f9f9f9; padding:15px;">[AD_SPACE]</div> twice.
    Start with: {image_html}"""
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "meta-llama/llama-3.1-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    
    response = requests.post(url, headers=headers, json=data).json()
    return response['choices'][0]['message']['content'].replace("```html", "").replace("```", "").strip()

# --- মেইন লজিক ---
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
run_index = int(os.environ.get("GITHUB_RUN_NUMBER", 1)) - 1
cat = CATEGORIES[run_index % len(CATEGORIES)]

content = generate_content(cat)
msg = EmailMessage()
msg['Subject'] = f"Expert Guide: {cat} 2026"
msg['From'] = sender_email
msg['To'] = recipient_email
msg.set_content(content, subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, EMAIL_PASS)
    smtp.send_message(msg)
        
