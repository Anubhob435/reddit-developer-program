import os
from dotenv import load_dotenv
import praw
from llm_gemini import GeminiAPI

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

# Step 1: Get top 5 trending posts from Reddit front page (r/all)
trending_posts = list(reddit.subreddit("all").hot(limit=5))

print("🔥 Top Trending Topics:\n")

trending_keywords = []
for i, post in enumerate(trending_posts, start=1):
    keyword = post.title.split(" ")[0:4]  # Use first few words as a simple topic
    topic = " ".join(keyword)
    trending_keywords.append(topic)
    print(f"{i}. {topic}")

print("\n🔍 Searching top 2 posts for each topic...\n")

# Step 2: Search Reddit for each trending topic
all_reddit_data = []  # Collect all data for story generation

for topic in trending_keywords:
    print(f"🔎 Topic: {topic}")
    search_results = reddit.subreddit("all").search(topic, sort="top", time_filter="day", limit=2)
    
    topic_data = {
        "topic": topic,
        "posts": []
    }

    for post in search_results:
        print(f" - {post.title} (r/{post.subreddit}) | 👍 {post.score} upvotes")
        
        # Collect post data
        post_data = {
            "title": post.title,
            "subreddit": str(post.subreddit),
            "score": post.score,
            "comments": []
        }

        # Optional: Print top-level comment as a "sub post"
        post.comments.replace_more(limit=0)
        top_comments = post.comments[:1]
        for comment in top_comments:
            comment_text = comment.body[:150]
            print(f"   💬 Top Comment: {comment_text}...\n")
            post_data["comments"].append(comment_text)
        
        topic_data["posts"].append(post_data)

    all_reddit_data.append(topic_data)
    print("-" * 60)

# Step 3: Generate a story based on all collected Reddit data
print("\n📚 Generating story from Reddit trends...\n")

try:
    gemini = GeminiAPI()
    
    # Prepare the data summary for the story prompt
    data_summary = "Here are the trending topics and posts from Reddit:\n\n"
    
    for topic_data in all_reddit_data:
        data_summary += f"**Topic: {topic_data['topic']}**\n"
        for post in topic_data['posts']:
            data_summary += f"- Post: {post['title']} (r/{post['subreddit']}, {post['score']} upvotes)\n"
            for comment in post['comments']:
                data_summary += f"  Comment: {comment}...\n"
        data_summary += "\n"
    
    # Create story generation prompt
    story_prompt = f"""Based on the following trending Reddit topics and discussions, create an engaging short story that weaves together these real-world trends and conversations. Make it creative and interesting while incorporating the themes and topics mentioned:

{data_summary}

Please write a cohesive story that connects these trending topics in a creative narrative. The story should be engaging and reflect the current zeitgeist captured in these Reddit discussions."""

    print("🤖 Asking AI to generate story...")
    story = gemini.generate_content(
        story_prompt,
        temperature=1.2,  # Higher creativity
        topP=0.9
    )
    
    if story:
        print("\n" + "="*80)
        print("📖 GENERATED STORY BASED ON REDDIT TRENDS")
        print("="*80)
        print(story)
        print("="*80)
    else:
        print("❌ Failed to generate story")
        
except ValueError as e:
    print(f"❌ {e}")
    print("Please add GEMINI_API_KEY to your .env file")
except Exception as e:
    print(f"❌ Error generating story: {e}")

