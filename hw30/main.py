import os
import time
import requests
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

file_handler = logging.FileHandler("app.log", encoding="utf-8")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[file_handler, logging.StreamHandler()])
logger = logging.getLogger(__name__)

load_dotenv()

OPEN_WEATHER_API = os.getenv("OPEN_WEATHER_API")
EXCHANGE_RATE_API = os.getenv("EXCHANGE_RATE_API")
THE_CAT_API = os.getenv("THE_CAT_API")

AWAITING_CITY = 1


def main():
    bot_token = os.getenv("TG_BOT_TOKEN")
    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cat", cat_command))
    app.add_handler(CommandHandler("currency", currency_command))

    weather_conv = ConversationHandler(
        entry_points=[CommandHandler("weather", weather_command)],
        states={
            AWAITING_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_weather)]
        },
        fallbacks=[CommandHandler("cancel", cancel_command)]
    )
    app.add_handler(weather_conv)

    print("Bot started")
    logger.info("Bot started")
    app.run_polling()
    print("Bot stopped")
    logger.info("Bot stopped")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actions after /start entered by user"""
    await update.message.reply_text("Greetings! Use /help to see available commands")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actions after /help entered by user, shows every available command"""
    await update.message.reply_text(
        "/help - shows all available commands\n"
        "/cancel - cancels any dialog\n"
        "/weather - shows weather information about chosen city\n"
        "/cat - cat\n"
        "/currency - shows current USD and EUR exchange rates relatively to UAH"
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actions after /cancel entered by user, cancels any dialog"""
    return ConversationHandler.END


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Actions after /weather entered by user, then goes to process_weather"""
    await update.message.reply_text("Enter city: ")
    return AWAITING_CITY


async def process_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts after weather_command (/weather), processes request, info from openweather, replies with:
    request time, location, temperature, humidity and description
    if everything was successful"""
    city = update.message.text
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_API}&units=metric"
    start_time = time.time()

    try:
        response = requests.get(url)
        data = response.json()

        execution_time = time.time() - start_time

        if response.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            reply = (
                f"Request time: {time.strftime('%D %I:%M %p')}\n"
                f"Location: {city.capitalize()}\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%\n"
                f"Overall weather description: {description.capitalize()}"
            )
            await update.message.reply_text(reply)
            logger.info(f"Successful request for '{city}'. Latency: {execution_time:.3f}")
        else:
            await update.message.reply_text(f"City '{city}' not found")
            logger.warning(
                f"City '{city}' not found. Status code: {response.status_code}. Timestamp: {execution_time:.3f}")

    except requests.exceptions.RequestException as e:
        execution_time = time.time() - start_time
        await update.message.reply_text(f"Error: {e}")
        logger.error(f"Error for city '{city}': {e}. Timestamp: {execution_time:.3f}")

    return ConversationHandler.END


async def cat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends and processes a cat picture after /cat etered by user"""
    url = "https://api.thecatapi.com/v1/images/search"
    start_time = time.time()

    try:
        response = requests.get(url)
        data = response.json()

        execution_time = time.time() - start_time

        if response.status_code == 200:
            cat_url = data[0]['url']

            logger.info(f"Success cat request. Latency: {execution_time:.3f}")

            await update.message.reply_photo(photo=cat_url)
        else:
            logger.warning(f"Unsuccessful cat request. Status code: {response.status_code}")
            await update.message.reply_text("Cat request error. Timestamp: {execution_time:.3f}")

    except requests.exceptions.RequestException as e:
        execution_time = time.time() - start_time
        logger.error(f"Error: {e}. Timestamp: {execution_time:.3f}")
    return ConversationHandler.END


async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends and processes currency request after /currency entered by user"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API}/latest/UAH"
    start_time = time.time()

    try:
        response = requests.get(url)
        data = response.json()

        execution_time = time.time() - start_time

        if response.status_code == 200 and data.get("result") == "success":
            usd_rate = data['conversion_rates']['USD']
            eur_rate = data['conversion_rates']['EUR']

            uah_per_usd = 1 / usd_rate
            uah_per_eur = 1 / eur_rate

            reply = (
                f"Request time: {time.strftime('%D %I:%M %p')}\n"
                f"1 USD = {uah_per_usd:.2f} UAH\n"
                f"1 EUR = {uah_per_eur:.2f} UAH"
            )

            logger.info(f"Successful currency request. Latency: {execution_time:.3f}")
            await update.message.reply_text(reply)
        else:
            logger.warning(f"Unsuccessful currency request. Status code: {response.status_code}")
            await update.message.reply_text("Error fetching currency data.")

    except requests.exceptions.RequestException as e:
        execution_time = time.time() - start_time
        logger.error(f"Currency API Error: {e}. Timestamp: {execution_time:.3f}")
        await update.message.reply_text(f"Error: {e}")


if __name__ == '__main__':
    main()
