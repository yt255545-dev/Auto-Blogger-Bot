import os
import requests

# ১. কনফিগারেশন ফাংশন (সব সেনসিটিভ তথ্য এখানে)
def get_config():
    return {
        "BLOG_ID": "8867375276332141549",
        "CLIENT_ID": os.environ.get("CLIENT_ID"),
        "CLIENT_SECRET": os.environ.get("CLIENT_SECRET"),
        "REFRESH_TOKEN": os.environ.get("REFRESH_TOKEN"),
        "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY"),
        "PEXELS_API_KEY": os.environ.get("PEXELS_API_KEY")
    }

# ২. টোকেন রিফ্রেশ ফাংশন
def get_new_access_token(config):
    url = "https://oauth2.googleapis.com/token"
    params = {
        "client_id": config["CLIENT_ID"],
        "client_secret": config["CLIENT_SECRET"],
        "refresh_token": config["REFRESH_TOKEN"],
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=params).json()
    return response['access_token']

# ৩. ছবি আনার ফাংশন
def get_pexels_image(config, query):
    try:
        headers = {"Authorization": config["PEXELS_API_KEY"]}
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
        data = requests.get(url, headers=headers).json()
        return data['photos'][0]['src']['large']
    except:
        return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

# ৪. কন্টেন্ট জেনারেশন ফাংশন
def generate_content(config, cat):
    img = get_pexels_image(config, cat)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {config['OPENROUTER_API_KEY']}", "Content-Type": "application/json"}
    prompt = f"Write an expert financial guide about '{cat}'. Use pure HTML tags. Start with <img src='{img}' style='width:100%;'>. Include SEO title, Meta Description, steps, pros/cons, and FAQ. No markdown."
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data).json()
    return response['choices'][0]['message']['content'].replace("```html", "").replace("```", "").strip()

# ৫. ব্লগার পাবলিশিং ফাংশন
def post_to_blogger(config, cat, content):
    token = get_new_access_token(config)
    url = f"https://www.googleapis.com/blogger/v3/blogs/{config['BLOG_ID']}/posts/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"kind": "blogger#post", "title": f"{cat} Expert Guide 2026", "content": content}
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code

# মূল রান ফাংশন
def main():
    config = get_config()
    CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
    run_number = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
    cat = CATEGORIES[(run_number - 1) % len(CATEGORIES)]
    
    content = generate_content(config, cat)
    status = post_to_blogger(config, cat, content)
    
    if status == 200:
        print(f"Success: {cat} posted!")
    else:
        print(f"Failed! Code: {status}")

if __name__ == "__main__":
    main()
        
