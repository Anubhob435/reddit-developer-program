import os
from dotenv import load_dotenv
import praw

# Load environment variables from .env file
load_dotenv()

# Get values from the environment
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

# Initialize PRAW
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

results = reddit.subreddit("all").search("openai", sort="top", limit=10)

for post in results:
    print(f"{post.title} (r/{post.subreddit}) - {post.score} upvotes")
