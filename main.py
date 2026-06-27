import os
import requests

# কনফিগারেশন - যা গিটহাব সিক্রেট থেকে আসবে
def get_config():
    return {
        "BLOG_ID": "8867375276332141549",
        "CLIENT_ID": os.environ.get("CLIENT_ID"),
        "CLIENT_SECRET": os.environ.get("CLIENT_SECRET"),
        "REFRESH_TOKEN": os.environ.get("REFRESH_TOKEN"),
        "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY"),
        "PEXELS_API_KEY": os.environ.get("PEXELS_API_KEY")
    }

# ১. নতুন এক্সেস টোকেন আনা
def get_new_access_token(config):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": config["CLIENT_ID"],
        "client_secret": config["CLIENT_SECRET"],
        "refresh_token": config["REFRESH_TOKEN"],
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data).json()
    if 'access_token' not in response:
        raise Exception(f"Token Error: {response}")
    return response['access_token']

# ২. ব্লগার-এ পোস্ট করা
def post_to_blogger(config, cat, content):
    token = get_new_access_token(config)
    url = f"https://www.googleapis.com/blogger/v3/blogs/{config['BLOG_ID']}/posts/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "kind": "blogger#post",
        "title": f"{cat} Expert Guide 2026",
        "content": content
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Blogger API Error: {response.text}")
    return response.status_code

# ৩. কন্টেন্ট জেনারেশন (আপনার পূর্বের প্রম্পট অনুযায়ী)
def generate_content(config, cat):
    # ছবি আনার লজিক
    try:
        headers = {"Authorization": config["PEXELS_API_KEY"]}
        res = requests.get(f"https://api.pexels.com/v1/search?query={cat}&per_page=1", headers=headers).json()
        img_url = res['photos'][0]['src']['large']
    except:
        img_url = "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {config['OPENROUTER_API_KEY']}", "Content-Type": "application/json"}
    prompt = f"Write a professional financial guide about '{cat}'. Use pure HTML tags. Start with <img src='{img_url}' style='width:100%;'>. Include SEO title, Meta Description, steps, pros/cons, and FAQ. No markdown."
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data).json()
    return response['choices'][0]['message']['content'].replace("```html", "").replace("```", "").strip()

# মেইন লজিক
if __name__ == "__main__":
    config = get_config()
    run_num = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
    cats = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
    cat = cats[(run_num - 1) % len(cats)]
    
    content = generate_content(config, cat)
    post_to_blogger(config, cat, content)
    print("Successfully Published!")
    
