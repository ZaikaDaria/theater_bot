import requests
import telebot
import os

from bs4 import BeautifulSoup
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://ft.org.ua/ua/performance/tartyuf"
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@dataclass
class Tortuf:
    performance_date: list[str]


def get_website_data():
    performance_list = []
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for item in soup.select(".performanceevents_item_info_date"):
            performance_dates = item.get_text(strip=True).split()[1]
            performance_list.append(Tortuf(performance_date=performance_dates))
        return performance_list


@bot.message_handler(commands=["list", ])
def send_message_to_telegram(message):
    performances = get_website_data()
    bot.reply_to(message, f"Тортюф: список всіх показів: {performances}")


@bot.message_handler(commands=["last", ])
def send_message_to_telegram(message):
    performances = get_website_data()
    perf_date = performances[-1].performance_date
    bot.reply_to(message, f"Тортюф: дата останнього показу: {str(perf_date)}")


# def echo_all(message):
#     bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.infinity_polling()
