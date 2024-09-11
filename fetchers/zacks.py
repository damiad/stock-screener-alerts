import requests


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
    score = calculate_score_zacks(stock_data["zacks_rank"])
    period = stock_data["updated"]
    return {score, period}


def get_zacks_recommendations(stock_symbol):
    zacks_url = f"https://quote-feed.zacks.com/index?t={stock_symbol}"
    response = requests.get(zacks_url)
    json_response = response.json()
    return format_data(stock_symbol, json_response)
