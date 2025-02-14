import telebot
import buttons
import requests
import datetime
from datetime import date, datetime, timedelta, time, timezone
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = str(os.getenv('API_KEY'))
bot = telebot.TeleBot(API_KEY)


API = str(os.getenv('API'))

list_of_error_messages = []

weather_details = {}

icon_code = {'01d': '☀️', '02d': '🌤️', '03d': '🌥️', '04d': '☁️',
             '09d': '🌦️', '10d': '🌧️', '11d': '⛈️', '13d': '❄️',
             '50d': '🌬️',

             '01n': '🌙', '02n': '☁️', '03n': '☁️', '04n': '☁️',
             '09n': '🌧️', '10n': '🌧️', '11n': '⛈️', '13n': '❄️',
             '50n': '💨'}


# Day icon	Night icon	Description
# ☀️ 01d.png ️ 	🌙 01n.png 	clear sky
# 🌤️ 02d.png ️ 	☁️ 02n.png  	few clouds
# 🌥️ 03d.png 	☁️ 03n.png 	scattered clouds
# ☁️ 04d.png 	☁️ 04n.png 	broken clouds
# 🌦️ 09d.png 	🌧 09n.png ️ 	shower rain
# 🌧️ 10d.png 	🌧️ 10n.png 	rain
# ⛈️ 11d.png 🌩️	⛈️ 11n.png 🌩️	thunderstorm
# ❄️ 13d.png 🌨️ ❄️	13n.png 🌨️	snow
# 🌬️ 50d.png 💨 🌬️	50n.png 💨	mist


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    bot.send_message(user_id, '🌤️ Welcome to WeatherBot! 🌦️', reply_markup=buttons.start_buttons())
    bot.register_next_step_handler(message, start_buttons_variants)


def start_buttons_variants(message):
    user_id = message.chat.id
    if message.text == '🗺️ Search Location':
        delete_error_messages(user_id)  # Deleting error messages
        bot.send_message(user_id, '🏙️ Please type in City name', reply_markup=buttons.back())
        bot.register_next_step_handler(message, typing_city_name)
    elif message.location:
        delete_error_messages(user_id)  # Deleting error messages
        bot.send_message(user_id, '🌏 Sharing location...', reply_markup=buttons.back())
        latitude = message.location.latitude
        longitude = message.location.longitude
        url = requests.get(f'https://api.openweathermap.org/data/2.5/weather?'
                           f'lat={latitude}&lon={longitude}&lang=en&&appid={API}&units=metric')
        if url.status_code == 200:
            weather_url_data = url.json()
            bot.send_message(user_id, f'🌉 Your location is '
                                      f'{weather_url_data['name']}, {weather_url_data['sys']['country']}\n\n'
                                      f'Please choose weather forecast by using buttons below 💬',
                             reply_markup=buttons.type_of_weather())
            weather_details['city_name'] = weather_url_data['name']
            weather_details['country'] = weather_url_data['sys']['country']
            bot.register_next_step_handler(message, type_of_weather)
        else:
            bot.send_message(user_id, '❌ ERROR: Could not find location\n\n'
                                      'Please try to check network connection 💬',
                             reply_markup=buttons.start_buttons())
            bot.register_next_step_handler(message, start_buttons_variants)
    else:
        user_response = message.message_id
        list_of_error_messages.append(user_response)
        bot_response = bot.send_message(user_id, '‼️Error ‼️\n\n'
                                                 '⬇️Please use buttons below ⬇️', reply_markup=buttons.start_buttons())
        list_of_error_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, start_buttons_variants)


def typing_city_name(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting error messages
        weather_details.clear()
        bot.send_message(user_id, '🌤️ Weather Menu 🌦️', reply_markup=buttons.start_buttons())
        bot.register_next_step_handler(message, start_buttons_variants)
    else:
        city_name = message.text.strip().lower()
        url = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}&units=metric')
        if url.status_code == 200:
            delete_error_messages(user_id)  # Deleting error messages
            city_name = city_name.capitalize()
            weather_url_data = url.json()
            bot.send_message(user_id, f'✅ "{city_name}" city name is successfully received\n\n'
                                      f'Please choose weather forecast by using buttons below 💬',
                             reply_markup=buttons.type_of_weather())
            weather_details['city_name'] = city_name
            weather_details['country'] = weather_url_data['sys']['country']
            bot.register_next_step_handler(message, type_of_weather)
        else:
            user_response = message.message_id
            list_of_error_messages.append(user_response)
            bot_response = bot.send_message(user_id, '❌ ERROR: City not found ❌\n\n'
                                                     'Please try again 💬')
            list_of_error_messages.append(bot_response.message_id)
            bot.register_next_step_handler(message, typing_city_name)


def type_of_weather(message):
    user_id = message.chat.id
    if message.text == '⬅️ Back':
        delete_error_messages(user_id)  # Deleting error messages
        weather_details.clear()
        bot.send_message(user_id, '🌤️ Weather Menu 🌦️', reply_markup=buttons.start_buttons())
        bot.register_next_step_handler(message, start_buttons_variants)
    elif message.text == '📆 Today':
        delete_error_messages(user_id)  # Deleting error messages
        today_weather_url = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q='
                                         f'{weather_details['city_name']}&appid={API}&units=metric')
        today_weather_data = today_weather_url.json()
        show_today_weather_details(message, user_id, today_weather_data)
    elif message.text == '📅 Tomorrow':
        delete_error_messages(user_id)  # Deleting error messages
        tomorrow_weather_url = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q='
                                            f'{weather_details['city_name']}&appid={API}&units=metric')
        tomorrow_weather = tomorrow_weather_url.json()
        show_tomorrow_weather_details(message, user_id, tomorrow_weather)
    elif message.text == '🗓️ For 5 days':
        delete_error_messages(user_id)  # Deleting error messages
        week_weather_url = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q='
                                        f'{weather_details['city_name']}&appid={API}&units=metric')
        week_weather = week_weather_url.json()
        show_5_days_weather(message, week_weather)
    else:
        user_response = message.message_id
        list_of_error_messages.append(user_response)
        bot_response = bot.send_message(user_id, '❌ ERROR: Invalid symbols ❌\n\n'
                                                 '⬇️ Please use buttons below ⬇️',
                                        reply_markup=buttons.type_of_weather())
        list_of_error_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, type_of_weather)


def show_today_weather_details(message, user_id, today_weather_data):
    today_timezone = today_weather_data['timezone']
    now_utc = datetime.now(timezone.utc)
    timezone_offset = timedelta(seconds=today_weather_data['timezone'])
    current_city_time = now_utc + timezone_offset
    formatted_today_date = current_city_time.strftime('%A, %-d %B')
    formatted_today_time = current_city_time.strftime('%I:%M %p')

    city = today_weather_data['name']
    country = today_weather_data['sys']['country']
    weather_details['country'] = country
    location = f'{city}, {country}'

    weather_icon = today_weather_data['weather'][0]['icon']
    weather_description = today_weather_data['weather'][0]['description'].capitalize()
    temperature = today_weather_data['main']['temp']
    humidity = today_weather_data['main']['humidity']
    sunrise_time = today_weather_data['sys']['sunrise']
    sunset_time = today_weather_data['sys']['sunset']
    today_sunrise_time = (datetime.fromtimestamp(sunrise_time, timezone.utc)
                          + timedelta(seconds=today_timezone))
    today_sunset_time = (datetime.fromtimestamp(sunset_time, timezone.utc)
                         + timedelta(seconds=today_timezone))
    sunrise_time = today_sunrise_time.strftime('%I:%M %p')
    sunset_time = today_sunset_time.strftime('%I:%M %p')

    bot.send_message(user_id, f'Today Weather Forecast:\n'
                              f'{'_' * 40}\n\n'
                              f'🏙️ Location: {location}\n\n'
                              f'📆 Date: {formatted_today_date}\n'
                              f'⌚️ Time: {formatted_today_time} ({city} time now)\n\n'
                              f'🌡️ Temperature: {icon_code[f'{weather_icon}']} {temperature:.0f}°C\n'
                              f'🌁 Condition: {weather_description}\n'
                              f'💧 Humidity: {humidity}%\n\n'
                              f'🌅 Sunrise: {sunrise_time}\n'
                              f'🌃 Sunset: {sunset_time}\n\n'
                              f'{'_' * 40}\n\n', reply_markup=buttons.change_location_or_get_weather_forecast())
    bot.register_next_step_handler(message, choose_change_or_continue)


def choose_change_or_continue(message):
    user_id = message.chat.id
    if message.text == '📌 Change location':
        delete_error_messages(user_id)  # Deleting error messages
        bot.send_message(user_id, '🌤️ Weather Menu 🌦️', reply_markup=buttons.start_buttons())
        bot.register_next_step_handler(message, start_buttons_variants)
        weather_details.clear()
    elif message.text == '🌦️ Weather Forecast ⛈️':
        delete_error_messages(user_id)  # Deleting error messages
        bot.send_message(user_id, f'Enter weather forecast for {weather_details['city_name']}, '
                                  f'{weather_details['country']} 💬',
                         reply_markup=buttons.type_of_weather())
        bot.register_next_step_handler(message, type_of_weather)
    else:
        user_response = message.message_id
        list_of_error_messages.append(user_response)
        bot_response = bot.send_message(user_id, '‼️Error ‼️\n\n'
                                                 '⬇️Please use buttons below ⬇️',
                                        reply_markup=buttons.type_of_weather())
        list_of_error_messages.append(bot_response.message_id)
        bot.register_next_step_handler(message, type_of_weather)


def show_tomorrow_weather_details(message, user_id, tomorrow_weather):
    today_date = date.today()
    tomorrow_date = today_date + timedelta(days=1)

    morning_time = time(9, 0, 0)
    tomorrow_morning_time = datetime.combine(tomorrow_date, morning_time)

    lunch_time = time(15, 0, 0)
    tomorrow_lunch_time = datetime.combine(tomorrow_date, lunch_time)

    evening_time = time(21, 0, 0)
    tomorrow_evening_time = datetime.combine(tomorrow_date, evening_time)

    for line in tomorrow_weather['list']:
        if line['dt_txt'] == tomorrow_morning_time.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['tomorrow_morning_time'] = line['dt_txt']
            weather_details['tomorrow_morning_time_temperature'] = line['main']['temp']
            weather_details['tomorrow_morning_time_description'] = line['weather'][0]['description']
            weather_details['tomorrow_morning_time_icon_code'] = line['weather'][0]['icon']
            weather_details['tomorrow_morning_time_humidity'] = line['main']['humidity']
            print(weather_details)
            break

    for line in tomorrow_weather['list']:
        if line['dt_txt'] == tomorrow_lunch_time.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['tomorrow_lunch_time'] = line['dt_txt']
            weather_details['tomorrow_lunch_time_temperature'] = line['main']['temp']
            weather_details['tomorrow_lunch_time_description'] = line['weather'][0]['description']
            weather_details['tomorrow_lunch_time_icon_code'] = line['weather'][0]['icon']
            weather_details['tomorrow_lunch_time_humidity'] = line['main']['humidity']
            print(weather_details)
            break

    for line in tomorrow_weather['list']:
        if line['dt_txt'] == tomorrow_evening_time.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['tomorrow_evening_time'] = line['dt_txt']
            weather_details['tomorrow_evening_time_temperature'] = line['main']['temp']
            weather_details['tomorrow_evening_time_description'] = line['weather'][0]['description']
            weather_details['tomorrow_evening_time_icon_code'] = line['weather'][0]['icon']
            weather_details['tomorrow_evening_time_humidity'] = line['main']['humidity']
            print(weather_details)
            break

    city = tomorrow_weather['city']['name']
    country = tomorrow_weather['city']['country']
    location = f'{city}, {country}'

    now_utc = datetime.now(timezone.utc)
    timezone_offset = timedelta(seconds=tomorrow_weather['city']['timezone'])
    current_city_time = now_utc + timezone_offset
    formatted_today_time = current_city_time.strftime('%I:%M %p')

    sunrise_time = tomorrow_weather['city']['sunrise']
    sunset_time = tomorrow_weather['city']['sunset']
    city_sunrise_time = datetime.fromtimestamp(sunrise_time, timezone.utc) + timezone_offset
    city_sunset_time = datetime.fromtimestamp(sunset_time, timezone.utc) + timezone_offset
    sunrise_time_formatted = city_sunrise_time.strftime('%I:%M %p')
    sunset_time_formatted = city_sunset_time.strftime('%I:%M %p')

    bot.send_message(user_id, f'Tomorrow Weather Forecast:\n'
                              f'{"_" * 40}\n\n'
                              f'🏙️ Location: {location}\n\n'
                              f'📆 Date: {tomorrow_date}\n'
                              f'⌚️ {city} time now: {formatted_today_time}\n\n\n'

                              f'{"-" * 35}\n'
                              f'⌚️ Morning:\n\n'
                              f'🌡️ Temperature: {icon_code[f"{weather_details["tomorrow_morning_time_icon_code"]}"]} '
                              f'{weather_details["tomorrow_morning_time_temperature"]:.0f}°C\n'
                              f'🌁 Condition: {weather_details["tomorrow_morning_time_description"]}\n'
                              f'💧 Humidity: {weather_details["tomorrow_morning_time_humidity"]}%\n'
                              f'{"-" * 35}\n\n\n'

                              f'{"-" * 35}\n'
                              f'⌚️ Afternoon:\n\n'
                              f'🌡️ Temperature: {icon_code[f"{weather_details['tomorrow_lunch_time_icon_code']}"]} '
                              f'{weather_details["tomorrow_lunch_time_temperature"]:.0f}°C\n'
                              f'🌁 Condition: {weather_details["tomorrow_lunch_time_description"]}\n'
                              f'💧 Humidity: {weather_details["tomorrow_lunch_time_humidity"]}%\n'
                              f'{"-" * 35}\n\n\n'

                              f'{"-" * 35}\n'
                              f'⌚️ Evening:\n\n'
                              f'🌡️ Temperature: {icon_code[f"{weather_details["tomorrow_evening_time_icon_code"]}"]} '
                              f'{weather_details["tomorrow_evening_time_temperature"]:.0f}°C\n'
                              f'🌁 Condition: {weather_details["tomorrow_evening_time_description"]}\n'
                              f'💧 Humidity: {weather_details["tomorrow_evening_time_humidity"]}%\n'
                              f'{"-" * 35}\n\n\n'

                              f'🌅 Sunrise: {sunrise_time_formatted}\n'
                              f'🌃 Sunset: {sunset_time_formatted}\n\n'
                              f'{"_" * 40}\n\n',
                     reply_markup=buttons.change_location_or_get_weather_forecast())

    bot.register_next_step_handler(message, choose_change_or_continue)


def show_5_days_weather(message, week_weather):
    user_id = message.chat.id
    today_date_first_day = date.today()

    delete_error_messages(user_id)  # Deleting error messages
    today_weather_url = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q='
                                     f'{weather_details['city_name']}&appid={API}&units=metric')
    today_weather_data = today_weather_url.json()

    now_utc = datetime.now(timezone.utc)
    timezone_offset = timedelta(seconds=today_weather_data['timezone'])
    current_city_time = now_utc + timezone_offset
    formatted_today_datetime = current_city_time.strftime('%Y-%m-%d %H:%M:%S')

    weather_details['first_day_datetime'] = formatted_today_datetime
    weather_details['first_day_temperature'] = today_weather_data['main']['temp']
    weather_details['first_day_humidity'] = today_weather_data['main']['humidity']
    weather_details['first_day_description'] = today_weather_data['weather'][0]['description'].capitalize()
    weather_details['first_day_icon_code'] = today_weather_data['weather'][0]['icon']

    second_day = today_date_first_day + timedelta(days=1)
    third_day = second_day + timedelta(days=1)
    fourth_day = third_day + timedelta(days=1)
    fifth_day = fourth_day + timedelta(days=1)

    morning_time = time(9, 0, 0)
    evening_time = time(21, 0, 0)

    second_day_time_morning = datetime.combine(second_day, morning_time)
    second_day_time_evening = datetime.combine(second_day, evening_time)

    third_day_time_morning = datetime.combine(third_day, morning_time)
    third_day_time_evening = datetime.combine(third_day, evening_time)

    fourth_day_time_morning = datetime.combine(fourth_day, morning_time)
    fourth_day_time_evening = datetime.combine(fourth_day, evening_time)

    fifth_day_time_morning = datetime.combine(fifth_day, morning_time)
    fifth_day_time_evening = datetime.combine(fifth_day, evening_time)

    for line in week_weather['list']:
        if line['dt_txt'] == second_day_time_morning.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['second_day_time_morning_datetime'] = line['dt_txt']
            weather_details['second_day_time_morning_temperature'] = line['main']['temp']
            weather_details['second_day_time_morning_humidity'] = line['main']['humidity']
            weather_details['second_day_time_morning_description'] = line['weather'][0]['description'].capitalize()
            weather_details['second_day_time_morning_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    for line in week_weather['list']:
        if line['dt_txt'] == second_day_time_evening.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['second_day_time_evening_datetime'] = line['dt_txt']
            weather_details['second_day_time_evening_temperature'] = line['main']['temp']
            weather_details['second_day_time_evening_humidity'] = line['main']['humidity']
            weather_details['second_day_time_evening_description'] = line['weather'][0]['description'].capitalize()
            weather_details['second_day_time_evening_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    for line in week_weather['list']:
        if line['dt_txt'] == third_day_time_morning.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['third_day_time_morning_datetime'] = line['dt_txt']
            weather_details['third_day_time_morning_temperature'] = line['main']['temp']
            weather_details['third_day_time_morning_humidity'] = line['main']['humidity']
            weather_details['third_day_time_morning_description'] = line['weather'][0]['description'].capitalize()
            weather_details['third_day_time_morning_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    for line in week_weather['list']:
        if line['dt_txt'] == third_day_time_evening.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['third_day_time_evening_datetime'] = line['dt_txt']
            weather_details['third_day_time_evening_temperature'] = line['main']['temp']
            weather_details['third_day_time_evening_humidity'] = line['main']['humidity']
            weather_details['third_day_time_evening_description'] = line['weather'][0]['description'].capitalize()
            weather_details['third_day_time_evening_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    for line in week_weather['list']:
        if line['dt_txt'] == fourth_day_time_morning.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['fourth_day_time_morning_datetime'] = line['dt_txt']
            weather_details['fourth_day_time_morning_temperature'] = line['main']['temp']
            weather_details['fourth_day_time_morning_humidity'] = line['main']['humidity']
            weather_details['fourth_day_time_morning_description'] = line['weather'][0]['description'].capitalize()
            weather_details['fourth_day_time_morning_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    for line in week_weather['list']:
        if line['dt_txt'] == fourth_day_time_evening.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['fourth_day_time_evening_datetime'] = line['dt_txt']
            weather_details['fourth_day_time_evening_temperature'] = line['main']['temp']
            weather_details['fourth_day_time_evening_humidity'] = line['main']['humidity']
            weather_details['fourth_day_time_evening_description'] = line['weather'][0]['description'].capitalize()
            weather_details['fourth_day_time_evening_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    for line in week_weather['list']:
        if line['dt_txt'] == fifth_day_time_morning.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['fifth_day_time_morning_datetime'] = line['dt_txt']
            weather_details['fifth_day_time_morning_temperature'] = line['main']['temp']
            weather_details['fifth_day_time_morning_humidity'] = line['main']['humidity']
            weather_details['fifth_day_time_morning_description'] = line['weather'][0]['description'].capitalize()
            weather_details['fifth_day_time_morning_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    for line in week_weather['list']:
        if line['dt_txt'] == fifth_day_time_evening.strftime('%Y-%m-%d %H:%M:%S'):
            weather_details['fifth_day_time_evening_datetime'] = line['dt_txt']
            weather_details['fifth_day_time_evening_temperature'] = line['main']['temp']
            weather_details['fifth_day_time_evening_humidity'] = line['main']['humidity']
            weather_details['fifth_day_time_evening_description'] = line['weather'][0]['description'].capitalize()
            weather_details['fifth_day_time_evening_icon_code'] = line['weather'][0]['icon']
            print(weather_details)
            break

    now_utc = datetime.now(timezone.utc)
    timezone_offset = timedelta(seconds=week_weather['city']['timezone'])
    current_city_time = now_utc + timezone_offset
    formatted_today_date = current_city_time.strftime('%A, %-d %B')
    formatted_today_time = current_city_time.strftime('%I:%M %p')

    first_day = today_date_first_day.strftime('%A, %-d %B')
    second_day = second_day.strftime('%A, %-d %B')
    third_day = third_day.strftime('%A, %-d %B')
    fourth_day = fourth_day.strftime('%A, %-d %B')
    fifth_day = fifth_day.strftime('%A, %-d %B')

    if 'fifth_day_time_morning_datetime' and 'fifth_day_time_evening_datetime' in weather_details:
        bot.send_message(user_id,
                         f'5 Days Forecast:\n'
                         f'{"_" * 40}\n\n'
                         f'🏙️ Location: {weather_details['city_name']}, {weather_details['country']}\n\n'
                         f'📆 Date: {formatted_today_date}\n'
                         f'⌚️ {weather_details['city_name']} time now: {formatted_today_time}\n\n\n'
                         
                         
                         f'{"-" * 35}\n'
                         f'📅 {first_day:<15}\n'
                         f'🌡️ Temperature: {icon_code[f"{weather_details['first_day_icon_code']}"]}'
                         f'{weather_details['first_day_temperature']:.0f}°C\n'
                         f'🌁 Condition: {weather_details['first_day_description']}\n'
                         f'💧 Humidity: {weather_details['first_day_humidity']}%r\n'
                         f'{"-" * 35}\n\n\n'
                         
                         f'{"-" * 35}\n'
                         f'📅 {second_day:<15}\n'
                         f'🌡️ Temperature: {icon_code[f'{weather_details['second_day_time_morning_icon_code']}']}'
                         f'{weather_details['second_day_time_morning_temperature']:.0f}°C / '
                         f'{icon_code[f"{weather_details['second_day_time_evening_icon_code']}"]} '
                         f'{weather_details['second_day_time_evening_temperature']:.0f}°C\n'
                         f'🌁 Condition: {weather_details['second_day_time_morning_description']}\n'
                         f'💧 Humidity: {weather_details['second_day_time_morning_humidity']}% / '
                         f' {weather_details['second_day_time_evening_humidity']}%\n'
                         f'{"-" * 35}\n\n\n'
    
                         f'{"-" * 35}\n'
                         f'📅 {third_day:<15}\n'
                         f'🌡️ Temperature: {icon_code[f'{weather_details['third_day_time_morning_icon_code']}']}'
                         f'{weather_details['third_day_time_morning_temperature']:.0f}°C / '
                         f'{icon_code[f"{weather_details['third_day_time_evening_icon_code']}"]} '
                         f'{weather_details['third_day_time_evening_temperature']:.0f}°C\n'
                         f'🌁 Condition: {weather_details['third_day_time_morning_description']}\n'
                         f'💧 Humidity: {weather_details['third_day_time_morning_humidity']}% / '
                         f' {weather_details['third_day_time_evening_humidity']}%\n'
                         f'{"-" * 35}\n\n\n'
    
                         f'{"-" * 35}\n'
                         f'📅 {fourth_day:<15}\n'
                         f'🌡️ Temperature: {icon_code[f'{weather_details['fourth_day_time_morning_icon_code']}']}'
                         f'{weather_details['fourth_day_time_morning_temperature']:.0f}°C / '
                         f'{icon_code[f"{weather_details['fourth_day_time_evening_icon_code']}"]} '
                         f'{weather_details['fourth_day_time_evening_temperature']:.0f}°C\n'
                         f'🌁 Condition: {weather_details['fourth_day_time_morning_description']}\n'
                         f'💧 Humidity: {weather_details['fourth_day_time_morning_humidity']}% / '
                         f' {weather_details['fourth_day_time_evening_humidity']}%\n'
                         f'{"-" * 35}\n\n\n'
    
                         f'{"-" * 35}\n'
                         f'📅 {fifth_day:<15}\n'
                         f'🌡️ Temperature: {icon_code[f'{weather_details['fifth_day_time_morning_icon_code']}']}'
                         f'{weather_details['fifth_day_time_morning_temperature']:.0f}°C / '
                         f'{icon_code[f"{weather_details['fifth_day_time_evening_icon_code']}"]} '
                         f'{weather_details['fifth_day_time_evening_temperature']:.0f}°C\n'
                         f'🌁 Condition: {weather_details['fifth_day_time_morning_description']}\n'
                         f'💧 Humidity: {weather_details['fifth_day_time_morning_humidity']}% / '
                         f' {weather_details['fifth_day_time_evening_humidity']}%\n'
                         f'{"-" * 35}\n\n\n'
                         
                         f'{"_" * 40}\n\n',

                         reply_markup=buttons.change_location_or_get_weather_forecast())
    else:
        bot.send_message(user_id, f'‼️ERROR: Weather Forecast for 5 days is invalid now ‼️\n\n'
                                  f'Please try again later 💬',
                         reply_markup=buttons.change_location_or_get_weather_forecast())

    bot.register_next_step_handler(message, choose_change_or_continue)


def delete_error_messages(user_id):
    if len(list_of_error_messages) > 0:
        for error_message in list_of_error_messages:
            bot.delete_message(user_id, error_message)
    list_of_error_messages.clear()


bot.infinity_polling()
