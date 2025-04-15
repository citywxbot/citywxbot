import openai
import requests
import os

# API keys stored in GitHub Secrets
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Secret for OpenAI API Key
TWITTER_API_KEY = os.getenv("API_KEY")  # Secret for Twitter API Key
TWITTER_API_SECRET = os.getenv("API_KEY_SECRET")  # Secret for Twitter API Key Secret
TWITTER_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Secret for Twitter Access Token
TWITTER_ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET")  # Secret for Twitter Access Token Secret

# Debugging step to verify keys are correctly loaded
if not all([OPENAI_API_KEY, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
    print("⚠️ Missing API credentials. Please check your environment variables.")
else:
    print(f"✅ API credentials loaded successfully.")

# Use ChatGPT to generate a weather-related tweet
def generate_weather_tweet():
    # Configure OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = """
    Generate a short tweet about the weather, 
    mentioning the sunny weather in California for top 10 populated cities. 
    Keep it simple and positive also include a positive quote in the beginning.
    """
    
    # Generate tweet using OpenAI's GPT model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that writes weather updates."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

# Function to get OAuth 2.0 bearer token
def get_twitter_bearer_token():
    url = "https://api.twitter.com/oauth2/token"
    auth = (TWITTER_API_KEY, TWITTER_API_SECRET)
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, auth=auth, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error getting bearer token: {response.status_code}")
        print(response.text)
        return None

# Function to authenticate and post tweet using v2 API
def tweet_forecast():
    # Ensure credentials are loaded
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        print("⚠️ Missing API credentials. Please check your environment variables.")
        return
    
    # Generate the tweet using ChatGPT
    tweet_text = generate_weather_tweet()
    
    # Twitter API v2 endpoint for creating tweets
    url = "https://api.twitter.com/2/tweets"
    
    # Get OAuth 1.0a authentication header
    from requests_oauthlib import OAuth1
    auth = OAuth1(
        TWITTER_API_KEY,
        TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_SECRET
    )
    
    # Create payload for the tweet
    payload = {"text": tweet_text}
    
    # Make the request to post the tweet
    response = requests.post(url, json=payload, auth=auth)
    
    # Check if successful
    if response.status_code == 201:
        print("Tweet posted successfully!")
        print(f"Tweet content: {tweet_text}")
    else:
        print(f"Error posting tweet: {response.status_code}")
        print(response.text)

# Run the bot when executed directly
if __name__ == "__main__":
    tweet_forecast()
