import requests
import tweepy
import os
from datetime import datetime

# API keys stored in GitHub Secrets
OWM_API_KEY = os.getenv("OWM_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

cities = {
    "Los Angeles": {"id": "5368361", "lat": 34.0522, "lon": -118.2437},
    "San Diego": {"id": "5391811", "lat": 32.7157, "lon": -117.1611},
    "San Jose": {"id": "5392171", "lat": 37.3382, "lon": -121.8863},
    "San Francisco": {"id": "5391959", "lat": 37.7749, "lon": -122.4194},
    "Fresno": {"id": "5350937", "lat": 36.7468, "lon": -119.7726},
    "Sacramento": {"id": "5389489", "lat": 38.5816, "lon": -121.4944},
    "Long Beach": {"id": "5367929", "lat": 33.7701, "lon": -118.1937},
    "Oakland": {"id": "5378538", "lat": 37.8044, "lon": -122.2711},
    "Bakersfield": {"id": "5325738", "lat": 35.3733, "lon": -119.0187},
    "Anaheim": {"id": "5323810", "lat": 33.8366, "lon": -117.9143},
}

def get_weather_history(city, start, end):
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={city['lat']}&lon={city['lon']}&type=hour&start={start}&end={end}&appid={OWM_API_KEY}"
    res = requests.get(url).json()
    if 'list' in res:
        temp = round(res['list'][0]['main']['temp'])
        desc = res['list'][0]['weather'][0]['description'].capitalize()
        return f"{temp}°C, {desc}"
    else:
        print(f"⚠️ Failed to get weather history: {res}")
        return "?"

def compose_tweet():
    # Use a timestamp for the current time range
    end = int(datetime.now().timestamp())
    start = end - 86400  # 24 hours ago
    lines = ["📍 Daily California Weather Update ☀️\n"]
    for city_name, city in cities.items():
        forecast = get_weather_history(city, start, end)
        lines.append(f"{city_name}: {forecast}")
    lines.append("\n#WeatherBot #CaliforniaWeather #DailyForecast")
    return "\n".join(lines)

def tweet_forecast():
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    )
    api = tweepy.API(auth)
    tweet = compose_tweet()
    api.update_status(tweet)

if __name__ == "__main__":
    tweet_forecast()
