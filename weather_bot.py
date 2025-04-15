import requests
import tweepy
import os

# API keys stored in GitHub Secrets
OWM_API_KEY = os.getenv("OWM_API_KEY")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Cities with their latitude and longitude
cities = {
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
    "San Diego": {"lat": 32.7157, "lon": -117.1611},
    "San Jose": {"lat": 37.7749, "lon": -122.4194},
    "San Francisco": {"lat": 37.7749, "lon": -122.4194},
    "Fresno": {"lat": 36.7468, "lon": -119.7726},
    "Sacramento": {"lat": 38.5816, "lon": -121.4944},
    "Long Beach": {"lat": 33.7701, "lon": -118.1937},
    "Oakland": {"lat": 37.8044, "lon": -122.2711},
    "Bakersfield": {"lat": 35.3733, "lon": -119.0187},
    "Anaheim": {"lat": 33.8366, "lon": -117.9143}
}

# Example timestamps for historical data (Unix timestamp format)
start_time = 1622512800  # Example start time
end_time = 1622599200  # Example end time

def get_weather(lat, lon):
    # Construct the historical weather URL with parameters
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&end={end_time}&appid={OWM_API_KEY}"
    
    # Fetch data from OpenWeatherMap API
    res = requests.get(url).json()
    
    if 'list' in res:
        temp = round(res['list'][0]['main']['temp'])  # Get the first record's temperature
        desc = res['list'][0]['weather'][0]['description'].capitalize()
        return f"{temp}°C, {desc}"
    else:
        print(f"⚠️ Failed to get weather data: {res}")
        return "?"

def compose_tweet():
    lines = ["📍 Daily California Weather Update ☀️\n"]
    for city, coords in cities.items():
        forecast = get_weather(coords["lat"], coords["lon"])
        lines.append(f"{city}: {forecast}")
    lines.append("\n#WeatherBot #CaliforniaWeather #DailyForecast")
    return "\n".join(lines)

def tweet_forecast():
    # Authenticate using Twitter API keys
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    )
    api = tweepy.API(auth)
    
    # Compose tweet and post it
    tweet = compose_tweet()
    api.update_status(tweet)

if __name__ == "__main__":
    tweet_forecast()
