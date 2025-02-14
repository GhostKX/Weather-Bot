# Telegram Weather-Bot 🌤️

A **Python-based Telegram bot** that provides real-time weather forecasts for any location. Users can get weather details for today, tomorrow, or the next 5 days. The bot supports location sharing and city name search, offering temperature, humidity, weather conditions, sunrise, and sunset times. Built using the **PyTelegramBotAPI** library and the **OpenWeatherMap API**, this bot is a comprehensive weather forecasting tool.

---

## Features

### Weather Forecasts
- **Today's Weather**: Get detailed weather information for the current day.
- **Tomorrow's Weather**: View weather predictions for the next day.
- **5-Day Forecast**: Access a 5-day weather outlook.

### Location Management
- **City Name Search**: Search for weather by typing in a city name.
- **Location Sharing**: Share your location to get weather updates for your area.

### Weather Details
- **Temperature**: Current and forecasted temperatures in Celsius.
- **Humidity**: Humidity levels for the selected location.
- **Weather Conditions**: Clear sky, rain, snow, thunderstorm, etc.
- **Sunrise & Sunset Times**: Accurate times for sunrise and sunset.

### User Interface
- **Interactive Buttons**: Easy navigation through button menus.
- **Step-by-step Process**: Guided weather forecast selection.
- **Error Handling**: Clear error messages and input validation.
- **Back Navigation**: Easy return to previous menus.

---

## Requirements

- Python 3.x
- PyTelegramBotAPI
- OpenWeatherMap API Key
- Datetime (for time calculations)

---

## Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/Weather-Bot.git
```

2. Install required dependencies
```bash
pip install -r requirements.txt
```

3. Configure the bot

- Create a .env file to store your Telegram API Key and OpenWeatherMap API Key:

```
API_KEY=your-telegram-bot-token
API=your-openweathermap-api-key
```

4. Navigate to the project directory
```bash
cd Telegram-WeatherBot
```

5. Run the bot
```bash
python PythonWeather_bot.py
```

## Usage

### Initial Setup
1. Start the bot with `/start`.
2. Choose an option:
   - **🗺️ Search Location**: Type in a city name.
   - **📍 Share Location**: Share your current location.

### Weather Forecasts
1. Select the type of forecast:
   - **📆 Today**: Get today's weather.
   - **📅 Tomorrow**: Get tomorrow's weather.
   - **🗓️ For 5 Days**: Get a 5-day weather forecast.

### Weather Details
- **Temperature**: Displayed in Celsius.
- **Humidity**: Shown as a percentage.
- **Weather Conditions**: Described with emojis and text.
- **Sunrise & Sunset Times**: Displayed in local time.


## Author

- Developed by **GhostKX**
- GitHub: **[GhostKX](https://github.com/GhostKX/Weather-Bot)**