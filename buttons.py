from telebot import types


def start_buttons():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    set_location_button = types.KeyboardButton('🗺️ Search Location')
    get_location_button = types.KeyboardButton('📍 Share Location', request_location=True)

    markup.row(set_location_button, get_location_button)
    return markup


def type_of_weather():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today_button = types.KeyboardButton('📆 Today')
    tomorrow_button = types.KeyboardButton('📅 Tomorrow')
    week_button = types.KeyboardButton('🗓️ For 5 days')
    back_button = types.KeyboardButton('⬅️ Back')

    markup.row(today_button, tomorrow_button, week_button)
    markup.row(back_button)
    return markup


def back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton('⬅️ Back')

    markup.row(back_button)
    return markup


def change_location_or_get_weather_forecast():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    change_location_button = types.KeyboardButton('📌 Change location')
    get_weather_forecast_button = types.KeyboardButton('🌦️ Weather Forecast ⛈️')

    markup.row(change_location_button, get_weather_forecast_button)
    return markup
