import requests
import tweepy
import os

# API keys stored in GitHub Secrets
OWM_API_KEY = os.getenv("OWM_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

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
    for city, cid in cities.items():
        forecast = get_weather(cid)
        lines.append(f"{city}: {forecast}")
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
