import os
from dotenv import load_dotenv
from fetchers.finnhub import get_finnhub_recommendations
from fetchers.zacks import get_zacks_recommendations
from alerts.pushover import send_pushover_notification

load_dotenv()
send_alert = os.getenv("send_alert")

# def get_iex_recommendations(stock_symbol):
#     iex_api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#     iex_url = f'https://cloud.iexapis.com/stable/stock/{stock_symbol}/recommendation-trends?token={iex_api_key}'
#     response = requests.get(iex_url)
#     return response.json()

# def get_yahoo_recommendations(stock_symbol):
#     yahoo_api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#     yahoo_url = f'https://yfapi.net/v11/finance/quoteSummary/recommendation-trends?symbol={stock_symbol}'
#     headers = {
#         'x-api-key': yahoo_api_key
#     }
#     response = requests.get(yahoo_url, headers=headers)
#     return response.json()

stock_symbols = ["AAPL", "MSFT", "GOOGL", "NVDA", "SMCI"]

for stock_symbol in stock_symbols:
    recommendations_finnhub = get_finnhub_recommendations(stock_symbol)
    recommendations_zacks = get_zacks_recommendations(stock_symbol)
    print(
        f"{stock_symbol}:\n finnhub: {recommendations_finnhub} \n zacks: {recommendations_zacks}"
    )

    if send_alert and send_alert.lower() == "true":
        message = f"{stock_symbol} Recommendations\nFinnhub: {recommendations_finnhub}\nZacks: {recommendations_zacks}"
        send_pushover_notification(message)
