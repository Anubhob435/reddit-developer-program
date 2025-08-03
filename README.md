# Reddit API Integration

A proper Python implementation for interacting with the Reddit API using OAuth2 authentication.

## Features

- ✅ Secure credential management using environment variables
- ✅ Proper OAuth2 authentication flow
- ✅ Error handling and status checking
- ✅ Reusable API client class
- ✅ Example usage for common operations

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Reddit App

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the details:
   - **Name**: Your app name
   - **App type**: Select "script"
   - **Description**: Brief description of your app
   - **About URL**: Can be left blank for scripts
   - **Redirect URI**: Use `http://localhost:8080` for scripts
4. Click "Create app"
5. Note down the **client ID** (under the app name) and **client secret**

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and fill in your credentials:
   ```
   REDDIT_CLIENT_ID=your_client_id_from_step_2
   REDDIT_CLIENT_SECRET=your_client_secret_from_step_2
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   REDDIT_USER_AGENT=YourAppName/1.0 by YourRedditUsername
   ```

### 4. Run the Application

```bash
python main.py
```

## Usage

The `RedditAPI` class provides several methods:

- `authenticate()` - Authenticate with Reddit and get access token
- `get_user_info()` - Get information about the authenticated user
- `get_subreddit_posts(subreddit, sort, limit)` - Get posts from a subreddit
- `make_authenticated_request(endpoint, method, **kwargs)` - Make custom API requests

## Example

```python
from main import RedditAPI

# Create API instance
reddit = RedditAPI()

# Authenticate
if reddit.authenticate():
    # Get user info
    user_info = reddit.get_user_info()
    print(f"Hello, {user_info['name']}!")
    
    # Get hot posts from r/python
    posts = reddit.get_subreddit_posts('python', sort='hot', limit=5)
    for post in posts['data']['children']:
        print(post['data']['title'])
```

## Security Notes

- Never commit your `.env` file to version control
- Use environment variables in production
- Consider using Reddit's OAuth2 flow for web applications
- The script uses the "password" grant type, suitable for personal scripts

## Rate Limiting

Reddit API has rate limits:
- 60 requests per minute for authenticated requests
- Be respectful and don't spam the API
- The client includes proper User-Agent headers as required

## Troubleshooting

- **401 Unauthorized**: Check your client ID, client secret, username, and password
- **403 Forbidden**: Your app might be rate limited or suspended
- **User-Agent errors**: Make sure your User-Agent follows Reddit's guidelines
- **Network errors**: Check your internet connection and Reddit's status

## API Documentation

For more information about Reddit's API, visit:
- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [Reddit API Rules](https://github.com/reddit-archive/reddit/wiki/API)
