import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

BASE_URL = "https://ft.org.ua/ua/performance/tartyuf"


class Tortuf:
    def __init__(self, performance_date):
        self.performance_date = performance_date

    def __repr__(self):
        return f"Tortuf(performance_date={self.performance_date})"


def get_website_data():
    performance_list = []
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        for item in soup.select(".performanceevents_item_info_date"):
            performance_dates = item.get_text(strip=True).split()[1]
            performance_list.append(Tortuf(performance_date=performance_dates))
        return performance_list


@app.route("/list")
def list_performances():
    performances = get_website_data()
    return f"Тортюф: список всіх показів: {performances}"


@app.route("/last")
def last_performance():
    performances = get_website_data()
    perf_date = performances[-1].performance_date
    return f"Тортюф: дата останнього показу: {str(perf_date)}"


if __name__ == "__main__":
    app.run(debug=True)
