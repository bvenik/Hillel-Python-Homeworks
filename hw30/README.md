# Telegram Utility Bot

## Description

Simple Telegram bot written in Python.

Features:

- Get weather information for a city.
- Get a random cat image.
- Get current USD and EUR exchange rates.
- Log successful and failed requests.

---

## APIs Used

- Telegram Bot API — bot interaction.
- OpenWeather API — weather information.
- ExchangeRate API — currency exchange rates.
- The Cat API — random cat images.

---

## Installation

Repository:
https://github.com/bvenik/Hillel-Python-Homeworks/tree/b5823d45ab7a8af32a68aeae68322a778a481aed/hw30

1. Clone the repository.

```bash
git clone https://github.com/bvenik/Hillel-Python-Homeworks.git
cd Hillel-Python-Homeworks/hw30
```

2. Install dependencies.

```bash
pip install python-telegram-bot requests python-dotenv
```

3. Create a `.env` file.

```env
TG_BOT_TOKEN=your_token
OPEN_WEATHER_API=your_key
EXCHANGE_RATE_API=your_key
THE_CAT_API=your_key
```

4. Run the program.

```bash
python main.py
```

---

## Available Commands

### /start

Starts the bot.

### /help

Shows all available commands.

### /weather

Shows weather information for a selected city.

Example:

```text
/weather
Kyiv
```

Output:

```text
Request time: 06/13/26 03:56 PM
Location: Kyiv
Temperature: 21.51°C
Humidity: 53%
Overall weather description: Few clouds
```

### /cat

Sends a random cat image.

Example:

```text
User:
/cat
```

Output:

![Cat](cat_example.png)

### /currency

Shows current USD and EUR exchange rates relative to UAH.

Example:

```text
/currency
```

Output:

```text
Request time: 06/13/26 04:22 PM
1 USD = 44.84 UAH
1 EUR = 51.89 UAH
```

---

## Logging

The application logs:

- Successful requests.
- Failed requests.
- API response time.
- Bot start and stop events.

Logs are stored in:

```text
app.log
```

---

## Security

API keys and bot token are stored in the `.env` file and are not included in the source code.

Add `.env` to `.gitignore`:

```text
.env
```
