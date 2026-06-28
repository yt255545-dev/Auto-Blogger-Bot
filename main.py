import smtplib
import os
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from dotenv import load_dotenv

# .env ফাইল থেকে বা এনভায়রনমেন্ট থেকে ডাটা লোড করা
load_dotenv()

# আপনার ক্রেডেনশিয়াল
sender_email = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS") # অবশ্যই App Password হতে হবে
recipient_email = "yt255545.finance1@blogger.com"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# ... (আপনার get_pexels_image ফাংশন আগের মতোই থাকবে) ...

def generate_content(cat):
    # আপনার আগের generate_content লজিক এখানে থাকবে
    # শুধু মনে রাখবেন, টেস্টিংয়ের জন্য [AD_SPACE] বা খুব বেশি হাইপারলিঙ্ক আপাতত প্রম্পট থেকে বাদ দিন।
    pass 

def send_professional_email(html_content, subject):
    # ইমেইলের স্ট্রাকচার তৈরি (Alternative - Text & HTML)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    
    # অ্যান্টি-স্প্যাম হেডার যুক্ত করা (খুবই গুরুত্বপূর্ণ)
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid()

    # একটি সাধারণ টেক্সট ভার্সন (স্প্যাম স্কোর কমানোর জন্য)
    text_content = "This is a new blog post. Please view it in a compatible HTML email client."
    
    # পার্টগুলো তৈরি করা
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')

    # মেসেজে যুক্ত করা (HTML পার্টটি শেষে যুক্ত করতে হয়)
    msg.attach(part1)
    msg.attach(part2)

    # ইমেইল পাঠানো
    try:
        print("সার্ভারের সাথে কানেক্ট করা হচ্ছে...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, email_pass)
            smtp.send_message(msg)
            print("✅ পোস্ট সফলভাবে পাঠানো হয়েছে এবং জিমেইল গ্রহণ করেছে!")
    except smtplib.SMTPResponseException as e:
        print(f"❌ সার্ভার রিজেক্ট করেছে! এরর কোড: {e.smtp_code}, মেসেজ: {e.smtp_error}")
    except Exception as e:
        print(f"❌ অন্য কোনো সমস্যা হয়েছে: {e}")

# স্ক্রিপ্ট রান করা
if __name__ == "__main__":
    cat = "Personal Finance" # টেস্টিংয়ের জন্য নির্দিষ্ট করে দিন
    # html_content = generate_content(cat) 
    
    # ⚠️ প্রথমবার টেস্ট করার জন্য নিচের সাধারণ HTML টি ব্যবহার করুন:
    test_html = """
    <h2>Test Post for Blogger</h2>
    <p>This is a simple test post to check if the email block is resolved.</p>
    """
    
    send_professional_email(test_html, "My Test Blog Post 2026")
            
