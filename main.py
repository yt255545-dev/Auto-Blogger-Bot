import os
import requests

# আপনার দেয়া তথ্যসমূহ
BLOG_ID = "8867375276332141549" # আপনার ব্লগের আইডি
API_KEY = "AIzaSyDppKsZKlyJegc3yCi2AQw-0_Jwj3Qlqug"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN") # এটি গিটহাব সিক্রেটে সেভ করবেন
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")

def get_pexels_image(query):
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        data = requests.get(url, headers=headers).json()
        return data['photos'][0]['src']['large']
    except:
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

def generate_content(cat):
    img = get_pexels_image(cat)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    
    prompt = f"Write an expert financial guide about '{cat}'. Use pure HTML tags. Start with <img src='{img}' style='width:100%;'>. Include SEO title, Meta Description, steps, pros/cons, and FAQ. No markdown, no stars, no hashes."
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data).json()
    return response['choices'][0]['message']['content'].replace("```html", "").replace("```", "").strip()

# ব্লগার API-তে পোস্ট করার ফাংশন
def post_to_blogger(cat, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/?key={API_KEY}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "kind": "blogger#post",
        "title": f"{cat} Expert Guide 2026",
        "content": content
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# রান করা
CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
cat = CATEGORIES[(int(os.environ.get("GITHUB_RUN_NUMBER", 1)) - 1) % len(CATEGORIES)]

content = generate_content(cat)
result = post_to_blogger(cat, content)

print(result)
                                                         
