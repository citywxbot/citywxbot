import requests
import tweepy
import os

# API keys stored in GitHub Secrets
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

cities = {
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
    "San Diego": {"lat": 32.7157, "lon": -117.1611},
    "San Jose": {"lat": 37.7749, "lon": -122.4194},
    "San Francisco": {"lat": 37.7749, "lon": -122.4194},
    "Fresno": {"lat": 36.7378, "lon": -119.7871},
    "Sacramento": {"lat": 38.5816, "lon": -121.4944},
    "Long Beach": {"lat": 33.7683, "lon": -118.1950},
    "Oakland": {"lat": 37.8044, "lon": -122.2711},
    "Bakersfield": {"lat": 35.3733, "lon": -119.0187},
    "Anaheim": {"lat": 33.8366, "lon": -117.9143}
}

def get_weather(city_data):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city_data['lat']}&longitude={city_data['lon']}&hourly=temperature_2m,weathercode"
    res = requests.get(url).json()
    if 'hourly' in res:
        temp = round(res['hourly']['temperature_2m'][0])  # Gets the temperature at the first available time point
        desc = res['hourly']['weathercode'][0]  # Weather description (code)
        # Translate weather code to description (for example)
        weather_descriptions = {
            0: "Clear sky", 1: "Partly cloudy", 2: "Cloudy", 3: "Overcast", 51: "Light rain", 52: "Moderate rain",
            53: "Heavy rain", 61: "Showers", 63: "Heavy showers"
        }
        desc = weather_descriptions.get(desc, "Unknown weather")
        return f"{temp}°C, {desc}"
    else:
        print(f"⚠️ Failed to get weather data: {res}")
        return "?"

def compose_tweet():
    lines = ["📍 Daily California Weather Update ☀️\n"]
    for city, city_data in cities.items():
        forecast = get_weather(city_data)
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
