import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment
access_token = os.getenv("REDDIT_ACCESS_TOKEN")

# Headers for Reddit API call
headers = {
    "Authorization": f"bearer {access_token}",
    "User-Agent": "TestScript/0.1 by your_reddit_username"
}

# Make a test request
url = "https://oauth.reddit.com/api/announcements/v1" 
response = requests.get(url, headers=headers)

# Output
if response.status_code == 200:
    print("✅ Token worked! Your account info:")
    print(response.json())
else:
    print(f"❌ Error {response.status_code}: {response.text}")
