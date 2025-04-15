import requests
import tweepy
import os

# API keys stored in GitHub Secrets
OWM_API_KEY = os.getenv("WEATHERBIT_API_KEY")  # Secret for Weatherbit API Key
TWITTER_API_KEY = os.getenv("API_KEY")  # Secret for Twitter API Key
TWITTER_API_SECRET = os.getenv("API_KEY_SECRET")  # Secret for Twitter API Key Secret
TWITTER_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Secret for Twitter Access Token
TWITTER_ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET")  # Secret for Twitter Access Token Secret

# Debugging step to verify keys are correctly loaded
if not all([OWM_API_KEY, TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
    print("⚠️ Missing API credentials. Please check your environment variables.")

cities = {
    "Los Angeles": "5368361",
    "San Diego": "5391811",
    "San Jose": "5392171",
    "San Francisco": "5391959",
    "Fresno": "5350937",
    "Sacramento": "5389489",
    "Long Beach": "5367929",
    "Oakland": "5378538",
    "Bakersfield": "5325738",
    "Anaheim": "5323810"
}

def get_weather(city_name):
    # Weatherbit API endpoint for current weather
    url = f"https://api.weatherbit.io/v2.0/current?city={city_name}&key={OWM_API_KEY}&units=M"
    res = requests.get(url).json()
    
    if 'data' in res:
        # Extract temperature and description
        temp = round(res['data'][0]['temp'])
        desc = res['data'][0]['weather']['description'].capitalize()
        return f"{temp}°C, {desc}"
    else:
        print(f"⚠️ Failed to get weather data: {res}")
        return "?"

def compose_tweet():
    lines = ["📍 Daily California Weather Update ☀️\n"]
    for city in cities.keys():
        forecast = get_weather(city)
        lines.append(f"{city}: {forecast}")
    lines.append("\n#WeatherBot #CaliforniaWeather #DailyForecast")
    return "\n".join(lines)

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

    # Create and send the tweet
    tweet = compose_tweet()
    api.update_status(tweet)

# Ensure this is at the bottom of the script
if __name__ == "__main__":
    tweet_forecast()  # This ensures the bot posts a tweet when you run it
