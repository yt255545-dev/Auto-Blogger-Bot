import os
import requests

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
    params = {
        "client_id": config["CLIENT_ID"],
        "client_secret": config["CLIENT_SECRET"],
        "refresh_token": config["REFRESH_TOKEN"],
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=params)
    res_json = response.json()
    
    # এরর বোঝার জন্য এটি প্রিন্ট করবে
    if 'access_token' not in res_json:
        print(f"গুগল এরর দিয়েছে: {res_json}")
        raise KeyError("গুগল এক্সেস টোকেন পাঠায়নি। আপনার REFRESH_TOKEN ভুল হতে পারে।")
    
    return res_json['access_token']

# ... (বাকি ফাংশন আগের মতোই থাকবে)
