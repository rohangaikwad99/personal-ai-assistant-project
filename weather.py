import requests
def get_weather(city, api_key="Your-API-Key"):
    try:
        # API URL for current weather data
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        # Sending the GET request
        response = requests.get(url)
        data = response.json()

        # If city not found
        if data.get("cod") != 200:
            return f"Sorry, I couldn't find the weather details for {city}. Please try again."

        # Extract relevant data
        city_name = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Return formatted weather information
        weather_report = (f"Weather in {city_name}, {country}:\n"
                          f"- Temperature: {temperature}°C\n"
                          f"- Condition: {description.capitalize()}\n"
                          f"- Humidity: {humidity}%\n"
                          f"- Wind Speed: {wind_speed} m/s")
        return weather_report
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while fetching the weather data."
