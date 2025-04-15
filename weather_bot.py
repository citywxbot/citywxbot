import requests
import tweepy
import os

# API keys stored in GitHub Secrets
OWM_API_KEY = os.getenv("WEATHERSTACK_API_KEY")  # Secret for WeatherStack API Key
TWITTER_API_KEY = os.getenv("API_KEY")  # Secret for Twitter API Key
TWITTER_API_SECRET = os.getenv("API_KEY_SECRET")  # Secret for Twitter API Key Secret
TWITTER_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Secret for Twitter Access Token
TWITTER_ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET")  # Secret for Twitter Access Token Secret

# Debugging step to verify keys are correctly loaded
print(f"OWM API Key: {OWM_API_KEY}")
print(f"Twitter API Key: {TWITTER_API_KEY}")
print(f"Twitter API Secret: {TWITTER_API_SECRET}")
print(f"Twitter Access Token: {TWITTER_ACCESS_TOKEN}")
print(f"Twitter Access Token Secret: {TWITTER_ACCESS_SECRET}")

# Cities and their codes
cities = {
    "Los Angeles": "Los Angeles",
    "San Diego": "San Diego",
    "San Jose": "San Jose",
    "San Francisco": "San Francisco",
    "Fresno": "Fresno",
    "Sacramento": "Sacramento",
    "Long Beach": "Long Beach",
    "Oakland": "Oakland",
    "Bakersfield": "Bakersfield",
    "Anaheim": "Anaheim"
}

def get_weather(city_name):
    url = f"http://api.weatherstack.com/current?access_key={OWM_API_KEY}&query={city_name}"
    res = requests.get(url).json()
    if 'current' in res:
        temp = round(res['current']['temperature'])
        desc = res['current']['weather_descriptions'][0].capitalize()
        return f"{temp}°C, {desc}"
    else:
        print(f"⚠️ Failed to get weather data: {res}")
        return "?"

def compose_tweet():
    lines = ["📍 Daily California Weather Update ☀️\n"]
    for city in cities:
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
