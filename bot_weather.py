import telebot
import requests

TELEGRAM_API_KEY = 'YOUR_TELEGRAM_BOT_TOKEN'
OPENWEATHER_API_KEY = 'YOUR_OPENWEATHER_API_KEY'

bot = telebot.TeleBot(TELEGRAM_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.reply_to(message, "🌦️ Hi! Send me a city name and I'll tell you the current temperature.")

@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}"
    try:
        res = requests.get(url)
        data = res.json()

        if data["cod"] == 200:
            kelvin_temp = data['main']['temp']
            celsius_temp = kelvin_temp - 273.15
            bot.reply_to(message, f"🌡️ Current temperature in {city} is {celsius_temp:.2f}°C.")
        else:
            bot.reply_to(message, "❌ Sorry, I couldn't find that city.")
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ Something went wrong. Try again.")

bot.polling()
