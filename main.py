import requests
from datetime import date, timedelta, datetime
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": YOUR_API,

}

response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()
if datetime.isoweekday(datetime.today()) == 1:
    yesterday = date.today() - timedelta(days=3)
    day_before_yesterday = date.today() - timedelta(days=4)
elif datetime.isoweekday(datetime.today()) == 2:
    yesterday = date.today() - timedelta(days=1)
    day_before_yesterday = date.today() - timedelta(days=4)
elif datetime.isoweekday(datetime.today()) == 7:
    yesterday = date.today() - timedelta(days=2)
    day_before_yesterday = date.today() - timedelta(days=3)
else:
    yesterday = date.today() - timedelta(days=1)
    day_before_yesterday = date.today() - timedelta(days=2)

yesterday_close_price = data["Time Series (Daily)"][str(yesterday)]['4. close']

day_before_yesterday_close_price = data["Time Series (Daily)"][str(day_before_yesterday)]['4. close']
positive_difference = abs(float(yesterday_close_price) - float(day_before_yesterday_close_price))

percentage_difference = positive_difference / float(day_before_yesterday_close_price) * 100

if float(yesterday_close_price) > float(day_before_yesterday_close_price):
    positive_or_negative = "🔺"
else:
    positive_or_negative = "🔻"

NEWS_APIKEY = YOUR_API
newparameters = {
    "q": COMPANY_NAME,
    "from": str(date.today()),
    "sortBy": "popularity",
    "apiKey": NEWS_APIKEY,
}

news_response = requests.get(NEWS_ENDPOINT, params=newparameters)
news_data = news_response.json()

first_three_news_data = news_data["articles"][:3]

new_list = {
    "stocks": round(percentage_difference),
    "description": [],
    "url": [],
}
for i in range(0, 3):
    description = first_three_news_data[i]['description']
    url = first_three_news_data[i]['url']
    new_list["description"].append(description)
    new_list["url"].append(url)

TWILIO_SID = YOUR_SID
TWILIO_AUTHTOKEN = YOUR_TOKEN
TWILIO_PHONE = YOUR_PHONE

client = Client(TWILIO_SID, TWILIO_AUTHTOKEN)

for i in range(0, 3):
    message = client.messages \
                    .create(
                         body=f"{STOCK_NAME}: {positive_or_negative}{new_list['stocks']}%\n{new_list['description'][i]}\n{new_list['url'][i]}",
                         from_=TWILIO_PHONE,
                         to=YOUR_PHONE
                     )
