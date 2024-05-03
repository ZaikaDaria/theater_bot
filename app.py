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
    performance_date: str
    link: str


def get_website_data():
    performance_list = []
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for item in soup.select(".performanceevents_item"):
            performance_dates = item.select_one(".performanceevents_item_info_date").get_text(strip=True).split()[1]
            link_element = item.select_one(".button.hvr-shutter-out-horizontal")
            if link_element and link_element.has_attr("onclick"):
                link = link_element["onclick"].split("'")[1]
            else:
                link = None
            performance_list.append(Tortuf(performance_date=performance_dates, link=link))
        return performance_list


@bot.message_handler(commands=["tortuf", ])
def send_message_to_telegram(message):
    performances = get_website_data()
    if performances:
        performance_str = "\n".join([f"{perf.performance_date} [Купити квитки]({perf.link})" for perf in performances])
        bot.reply_to(message, f"Тортюф: список всіх показів:\n{performance_str}", parse_mode="Markdown")


@bot.message_handler(commands=["last"])
def send_message_to_telegram(message):
    performances = get_website_data()
    if performances:
        last_performance = performances[-1]
        perf_date = last_performance.performance_date
        link = last_performance.link
        if link:
            bot.reply_to(message, f"Тортюф: дата останнього показу: \n{perf_date} [Купити квитки]({link})",
                         parse_mode="Markdown")
        else:
            bot.reply_to(message, f"Тортюф: дата останнього показу: {perf_date}\nПосилання на квитки відсутнє.")
    else:
        bot.reply_to(message, "Немає даних про покази.")


if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)
