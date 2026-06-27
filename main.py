import smtplib
from email.message import EmailMessage
import os
import requests

# গিটহাব সিক্রেট থেকে ডাটা নেওয়া
email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT_EMAIL")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

# সিরিয়াল বাই সিরিয়াল ক্যাটাগরি নির্বাচন
# গিটহাব রান নাম্বার ব্যবহার করে এটি প্রতিবার ক্রমানুসারে পরের ক্যাটাগরি বেছে নেবে
run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 0))
CATEGORIES = [
    "Credit Cards", "Loans", "Banking", "Investing", 
    "Insurance", "Taxes", "Personal Finance"
]
cat = CATEGORIES[run_number % len(CATEGORIES)]

def get_image(query):
    if not PEXELS_API_KEY:
        return f"https://source.unsplash.com/1200x600/?{query}"
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        response = requests.get(url, headers=headers, timeout=10).json()
        if response.get('photos'):
            return response['photos'][0]['src']['large']
    except Exception:
        pass
    return f"https://source.unsplash.com/1200x600/?{query}"

def generate_content(category):
    image_url = get_image(category.replace(" ", "+"))
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}", 
        "Content-Type": "application/json"
    }
    
    # এআই-কে ফুল আর্টিকেল লেখার কড়া নির্দেশ
    prompt = f"""Write a fully detailed, highly engaging, and SEO-optimized finance blog post in English about '{category}'.
    
    CRITICAL RULES:
    1. Write the FULL article. Do not use placeholders like [Write here] or [Insert text]. You must provide the actual content.
    2. Output ONLY pure HTML. NO markdown, NO asterisks (** or *), NO hashes (#).
    3. Do NOT wrap the response in ```html or ``` blocks. Just start immediately with <h1>.
    
    REQUIRED STRUCTURE:
    <h1>{category}: The Ultimate Financial Guide for 2026</h1>
    <img src="{image_url}" alt="Complete guide to {category}" style="width:100%; border-radius:8px; margin-bottom: 20px;">
    
    <p><em>Meta Description: Discover the complete guide to {category} for 2026. Learn expert strategies, pros and cons, and common mistakes to manage your finances successfully.</em></p>
    
    <h2>Introduction</h2>
    <p>Write a compelling 3-paragraph introduction about the importance of {category} in modern finance.</p>
    
    <h2>Quick Answer (TL;DR)</h2>
    <p><strong>Summary:</strong> Write a 2-3 sentence quick summary of the entire topic.</p>
    
    <h2>How {category} Works</h2>
    <p>Write detailed paragraphs explaining the core concepts and mechanics clearly.</p>
    
    <h2>Step-by-Step Guide</h2>
    <ol>
        <li>Write a detailed explanation for step 1</li>
        <li>Write a detailed explanation for step 2</li>
        <li>Write a detailed explanation for step 3</li>
    </ol>
    
    <h2>Pros and Cons</h2>
    <ul>
        <li><strong>Pros:</strong> Detail 3 realistic benefits.</li>
        <li><strong>Cons:</strong> Detail 3 realistic drawbacks.</li>
    </ul>
    
    <h2>Common Mistakes to Avoid</h2>
    <p>Write about 3 common pitfalls people face and how to avoid them in detail.</p>
    
    <h2>Frequently Asked Questions</h2>
    <h3>What is the best way to manage {category}?</h3>
    <p>Provide a detailed expert answer.</p>
    <h3>Are there hidden risks?</h3>
    <p>Provide a detailed expert answer on potential risks.</p>
    
    <h2>Conclusion</h2>
    <p>Write a strong concluding paragraph with actionable advice for the reader.</p>
    """
    
    data = {
        "model": "meta-llama/llama-3-8b-instruct", 
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, timeout=30)
    raw_content = response.json()['choices'][0]['message']['content']
    
    # যেকোনো মার্কডাউন বা স্টার চিহ্ন ফোর্সফুলি মুছে ফেলা
    clean_content = raw_content.replace("```html", "").replace("```", "").replace("**", "").replace("*", "").replace("#", "").strip()
    return clean_content

print(f"Generating SEO content for category: {cat} (Serial Run: {run_number})")
content = generate_content(cat)

msg = EmailMessage()
msg['Subject'] = f"Complete Guide to {cat} (2026 Edition)"
msg['From'] = email_user
msg['To'] = recipient
msg.set_content(content, subtype='html')

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)
    print("Success! 100% SEO Post published to Blogger.")
except Exception as e:
    print(f"Failed to send email: {e}")
    
