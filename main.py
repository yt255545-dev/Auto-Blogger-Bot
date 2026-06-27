import os
import requests
import json

def get_config():
    return {
        "BLOG_ID": "8867375276332141549",
        "CLIENT_ID": os.environ.get("CLIENT_ID"),
        "CLIENT_SECRET": os.environ.get("CLIENT_SECRET"),
        "REFRESH_TOKEN": os.environ.get("REFRESH_TOKEN"),
        "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY"),
        "PEXELS_API_KEY": os.environ.get("PEXELS_API_KEY")
    }

def get_new_access_token(config):
    url = "https://oauth2.googleapis.com/token"
    params = {"client_id": config["CLIENT_ID"], "client_secret": config["CLIENT_SECRET"], "refresh_token": config["REFRESH_TOKEN"], "grant_type": "refresh_token"}
    return requests.post(url, data=params).json()['access_token']

def get_pexels_image(config, query):
    try:
        headers = {"Authorization": config["PEXELS_API_KEY"]}
        data = requests.get(f"https://api.pexels.com/v1/search?query={query}&per_page=1", headers=headers).json()
        return data['photos'][0]['src']['large']
    except: return "https://images.pexels.com/photos/259132/pexels-photo-259132.jpeg"

def generate_content(config, cat):
    img = get_pexels_image(config, cat)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {config['OPENROUTER_API_KEY']}", "Content-Type": "application/json"}
    
    prompt = f"""Write an SEO-expert financial guide about '{cat}'. 
    CRITICAL RULES:
    1. Start with <img src='{img}' style='width:100%; border-radius:12px; margin-bottom:20px;'>
    2. Use ONLY HTML tags: <h1>, <h2>, <p>, <ul>, <li>. No markdown, no stars, no hashes.
    3. Include SEO Title, Meta Description (italicized), Introduction, How it Works, Pros & Cons Table, FAQ, and Conclusion.
    4. Ensure deep, high-quality content (800+ words). 
    5. Clean structure for Google Auto-ads."""
    
    data = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
    response = requests.post(url, headers=headers, json=data).json()
    return response['choices'][0]['message']['content'].replace("```html", "").replace("```", "").strip()

def main():
    config = get_config()
    CATEGORIES = ["Credit Cards", "Loans", "Banking", "Investing", "Insurance", "Taxes", "Personal Finance"]
    # গিটহাব রান নাম্বার অনুযায়ী সিরিয়াল মেইনটেইন
    run_num = int(os.environ.get("GITHUB_RUN_NUMBER", 1))
    cat = CATEGORIES[(run_num - 1) % len(CATEGORIES)]
    
    content = generate_content(config, cat)
    token = get_new_access_token(config)
    
    url = f"https://www.googleapis.com/blogger/v3/blogs/{config['BLOG_ID']}/posts/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"kind": "blogger#post", "title": f"{cat} Expert Guide 2026", "content": content}
    
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    main()
    
