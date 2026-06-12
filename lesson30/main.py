import requests

"""

response = requests.get('https://jsonplaceholder.typicode.com/todos/1')

#print(weather_response.status_code)
#print(weather_response.json())
#темп, вологість, опис
#temp humidity description
print(weather_response.json()['main']['temp'])
print(weather_response.json()['main']['humidity'])
print(weather_response.json()['weather'][0]['description'])"""

import telebot
import time

BOT_TOKEN = '8982254874:AAGw2ygJ-v0iqZgVNSaIkRkGdEQeE-JEIwM'
API_KEY = '965895b220dd92aed2d82f83342174d1'

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Enter city name to see the weather report")


@bot.message_handler(func=lambda message: True)
def get_weather(message):
    city = message.text

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']

            reply = (
                f"Request time: {time.strftime('%D %I:%M %p')}\n"
                f"City: {city.capitalize()}\n"
                f"Temperature: {temp} Celsius\n"
                f"Humidity: {humidity}%\n"
                f"Overall description: {description.capitalize()}"
            )
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, "City no found")

    except Exception as e:
        bot.reply_to(message, "Error ")


print("Bot started")
bot.infinity_polling()
print("Bot stopped")
