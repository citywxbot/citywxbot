import os
import openai
import tweepy
import requests

# WeatherStack API Key
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")  # Secret for WeatherStack API Key

# Twitter API keys
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Weather data
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
    url = f"http://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={city_id}"
    res = requests.get(url).json()
    if 'current' in res:
        temp = round(res['current']['temperature'])
        description = res['current']['weather_descriptions'][0]
        return f"{temp}°C, {description}"
    else:
        return "?"

def compose_weather_tweet():
    weather_data = {}
    for city, city_id in cities.items():
        forecast = get_weather(city_id)
        weather_data[city] = forecast

    # Generate tweet with ChatGPT
    tweet = generate_tweet(weather_data)
    return tweet

def generate_tweet(weather_data):
    # Create prompt for ChatGPT
    prompt = f"Generate a tweet about today's weather for the following cities in California: {weather_data}. Make the tweet friendly and engaging. Use emojis and relevant hashtags like #CaliforniaWeather #WeatherUpdate."

    # Make a request to ChatGPT to generate a tweet
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Return the generated tweet
    tweet = response.choices[0].text.strip()
    return tweet

def tweet_forecast():
    # Authenticate with Twitter
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)

    # Create and send the tweet
    tweet = compose_weather_tweet()
    api.update_status(tweet)
    print("Tweet posted successfully!")

# Ensure this is at the bottom of the script
if __name__ == "__main__":
    tweet_forecast()  # This ensures the bot posts a tweet when you run it
