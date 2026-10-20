import requests
import os

URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise RuntimeError("API_KEY is not set")


def get_weather(city):
    try:
        resp = requests.get(URL, params={"appid": WEATHER_API_KEY, "q": city, "units": "metric"}, timeout=10)
    except requests.RequestException:
        return f"Could not reach the weather service to check {city}"

    if resp.status_code == 400:
        return f"{city} is not a recognized city"
    resp.raise_for_status()

    data = resp.json()
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    wind_kph = data['wind']['speed']
    humidity = data['main']['humidity']
    return (
        f"Weather in {city} ({country}): "
        f"temperature is {temp}°C"
        f"speed of wind: {wind_kph} kph, Humidity is {humidity}%"
    )


TOOLS: dict = {
    "get_weather": get_weather
}
