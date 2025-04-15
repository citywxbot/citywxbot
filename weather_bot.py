import requests
import tweepy
import os

# API keys stored in GitHub Secrets
OWM_API_KEY = os.getenv("OPENWEATHER")  # Secret for OpenWeather API Key
TWITTER_API_KEY = os.getenv("API_KEY")  # Secret for Twitter API Key
TWITTER_API_SECRET = os.getenv("API_KEY_SECRET")  # Secret for Twitter API Key Secret
TWITTER_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Secret for Twitter Access Token
TWITTER_ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET")  # Secret for Twitter Access Token Secret

# Debugging step to verify keys are correctly loaded
print(f"API Key: {TWITTER_API_KEY}")
print(f"API Secret: {TWITTER_API_SECRET}")
print(f"Access Token: {TWITTER_ACCESS_TOKEN}")
print(f"Access Token Secret: {TWITTER_ACCESS_SECRET}")

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

def get_weather(city_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={OWM_API_KEY}&units=metric"
    res = requests.get(url).json()
    if 'main' in res:
        temp = round(res['main']['temp'])
        desc = res['weather'][0]['description'].capitalize()
        return f"{temp}°C, {desc}"
    else:
        print(f"⚠️ Failed to get weather data: {res}")
        return "?"

def compose_tweet():
    lines = ["📍 Daily California Weather Update ☀️\n"]

if __name__ == "__main__":
    tweet_forecast() 
