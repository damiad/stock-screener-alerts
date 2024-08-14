import requests
from dotenv import load_dotenv
import os

load_dotenv()
finnhub_api_key = os.getenv('finnhub_api_key')

def calculate_score(recommendation):
    win_strong_weight = 2
    win_weight = 1
    loose_strong_weight = -10
    loose_weight = -5
    loose_neutral_weight = -3
    scoreUp = (recommendation['strongBuy'] * win_strong_weight + recommendation['buy'] * win_weight) / ((recommendation['strongBuy'] * win_strong_weight + recommendation['buy'] * win_weight) - (recommendation['strongSell'] * loose_strong_weight + recommendation['sell'] * loose_weight + recommendation['hold'] * loose_neutral_weight))
    scoreDown = (recommendation['strongSell'] * win_strong_weight + recommendation['sell'] * win_weight) / ((recommendation['strongSell'] * win_strong_weight + recommendation['sell'] * win_weight) - (recommendation['strongBuy'] * loose_strong_weight + recommendation['buy'] * loose_weight + recommendation['hold'] * loose_neutral_weight))
    final_score = scoreUp if scoreUp > scoreDown else scoreDown * -1
    return round(final_score*100, 2)

def get_finnhub_recommendations(stock_symbol):
    finnhub_url = f'https://finnhub.io/api/v1/stock/recommendation?symbol={stock_symbol}&token={finnhub_api_key}'
    response = requests.get(finnhub_url)
    json_response = response.json()
    scores = []
    for recommendation in json_response:
        score = calculate_score(recommendation)
        scores.append({score, recommendation['period']})
    return scores

def calculate_score_zacks(zacks_rank):
    match int(zacks_rank):
        case 1:
            return 95
        case 2:
            return 80
        case 3:
            return 0
        case 4:
            return -80
        case 5:
            return -95
        case _:
            return None

def format_data(symbol, data):
    stock_data = data[symbol]
    score = calculate_score_zacks(stock_data['zacks_rank'])
    period = stock_data['updated']
    return {score, period}

def get_zacks_recommendations(stock_symbol):
    zacks_url = f'https://quote-feed.zacks.com/index?t={stock_symbol}'
    response = requests.get(zacks_url)
    json_response = response.json()
    return format_data(stock_symbol, json_response)


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


def send_pushover_notification(message):
    pushover_token = 'YOUR_PUSHOVER_APP_TOKEN'
    pushover_user_key = 'YOUR_PUSHOVER_USER_KEY'
    pushover_url = 'https://api.pushover.net/1/messages.json'
    
    pushover_data = {
        'token': pushover_token,
        'user': pushover_user_key,
        'message': message
    }
    requests.post(pushover_url, data=pushover_data)

stock_symbols = ['AAPL', 'MSFT', 'GOOGL','NVDA', 'SMCI']
# stock_symbols = ['AAPL']
for stock_symbol in stock_symbols:
    recommendations_finnhub = get_finnhub_recommendations(stock_symbol)
    recommendations_zacks = get_zacks_recommendations(stock_symbol)
    print(f'{stock_symbol}:\n finnhub: {recommendations_finnhub} \n zacks: {recommendations_zacks}')
    # print(f'{stock_symbol}: {recommendations}')

# for rec in recommendations:
#     if rec['buy'] > rec['sell']:
#         message = f"Stock {stock_symbol} Recommendation: Buy ({rec['buy']}) / Sell ({rec['sell']})"
#         send_pushover_notification(message)
