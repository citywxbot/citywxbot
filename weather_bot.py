import openai
import tweepy
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

# Use ChatGPT to generate a weather-related tweet (simplified prompt for weather updates)
def generate_weather_tweet():
    prompt = """
    Generate a short tweet about the weather, 
    mentioning the sunny weather in California for top 10 populated cities. 
    Keep it simple and positive also include a positive quote in the beginning.
    """

    # Generate tweet using OpenAI's GPT model
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # or use gpt-4 if available
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].text.strip()

# Function to authenticate and post tweet
def tweet_forecast():
    # Ensure credentials are loaded
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        print("⚠️ Missing API credentials. Please check your environment variables.")
        return

    # Authenticate with Twitter
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    )
    api = tweepy.API(auth)

    # Generate the tweet using ChatGPT
    tweet = generate_weather_tweet()

    # Post the tweet
    api.update_status(tweet)
    print("Tweet posted successfully!")

# Ensure this is at the bottom of the script
if __name__ == "__main__":
    tweet_forecast()  # This ensures the bot posts a tweet when you run it
