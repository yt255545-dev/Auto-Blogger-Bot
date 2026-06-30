import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import requests
import random

# কনফিগারেশন
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
INDEX_FILE = "category_index.txt"

def get_next_category():
    # ফাইল থেকে বর্তমান ইনডেক্স পড়া, না থাকলে ০ ধরা
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            try:
                index = int(f.read().strip())
            except:
                index = 0
    else:
        index = 0
    
    # বর্তমান ক্যাটাগরি নেওয়া
    category = CATEGORIES[index]
    
    # পরবর্তী ইনডেক্স আপডেট করা (এবং শেষে পৌঁছালে আবার ০ তে ফিরে যাওয়া)
    new_index = (index + 1) % len(CATEGORIES)
    with open(INDEX_FILE, "w") as f:
        f.write(str(new_index))
        
    return category

# ক্যাটাগরি সিলেক্ট করা
cat = get_next_category()
print(f"Selected Category: {cat}")

# এরপর আপনার আগের লজিক অনুযায়ী generate_seo_content এবং send_email কল করুন
# ...
