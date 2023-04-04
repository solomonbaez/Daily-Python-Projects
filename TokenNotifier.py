import requests
from datetime import datetime, timedelta
from twilio.rest import Client


# -----------------------------------------------------------------------#
# set parameters for alphavantage API
SYMBOL_NAME = "BTCUSD"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
SYMBOL_KEY = ""

symbol_params = {
    "apikey": SYMBOL_KEY,
    "symbol": SYMBOL_NAME,
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "outputsize": "compact"
}

# set parameters for newsapi API
COMPANY_NAME = "bitcoin"
NEWS_KEY = ""
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

news_params = {
    "apiKey": NEWS_KEY,
    "qInTitle": COMPANY_NAME,
    "sortBy": "publishedAt"
}

# set parameters for Twilio
SMS_STARTPOINT = ""
SMS_ENDPOINT = ""
ACCT_SID = ""
AUTH_TOKEN = ""

sms_client = Client(ACCT_SID, AUTH_TOKEN)

# get the three most recent dates
DATE = datetime.today()
D1 = (DATE - timedelta(days=1)).strftime("%Y-%m-%d")
D2 = (DATE - timedelta(days=2)).strftime("%Y-%m-%d")
# -----------------------------------------------------------------------#


# grab symbol prices
symbol_response = requests.get(STOCK_ENDPOINT, params=symbol_params)
prices = symbol_response.json()["Time Series (Daily)"]

# calculate price differential
diff = (float(prices[D1]["4. close"]) - float(prices[D2]["4. close"])) / float(prices[D1]["4. close"])

# if price has moved %5 in the last two days, collect recent news articles
if abs(diff) > 0.05:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)

    articles = news_response.json()["articles"][:3]

    for article in articles:
        msg = f"{SYMBOL_NAME}: {diff * 100}% \n " \
              f"Headline: {article['title']} \n " \
              f"Brief: {article['description']} \n " \
              f"Source: {article['source']['name']}"

        # send notifications
        sms_msg = sms_client.messages.create(body=msg,
                                             from_=SMS_STARTPOINT,
                                             to=SMS_ENDPOINT)