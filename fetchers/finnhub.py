import requests
import os
from dotenv import load_dotenv

load_dotenv()
finnhub_api_key = os.getenv("finnhub_api_key")


def calculate_score(recommendation):
    win_strong_weight = 2
    win_weight = 1
    loose_strong_weight = -10
    loose_weight = -5
    loose_neutral_weight = -3
    scoreUp = (
        recommendation["strongBuy"] * win_strong_weight
        + recommendation["buy"] * win_weight
    ) / (
        (
            recommendation["strongBuy"] * win_strong_weight
            + recommendation["buy"] * win_weight
        )
        - (
            recommendation["strongSell"] * loose_strong_weight
            + recommendation["sell"] * loose_weight
            + recommendation["hold"] * loose_neutral_weight
        )
    )
    scoreDown = (
        recommendation["strongSell"] * win_strong_weight
        + recommendation["sell"] * win_weight
    ) / (
        (
            recommendation["strongSell"] * win_strong_weight
            + recommendation["sell"] * win_weight
        )
        - (
            recommendation["strongBuy"] * loose_strong_weight
            + recommendation["buy"] * loose_weight
            + recommendation["hold"] * loose_neutral_weight
        )
    )
    final_score = scoreUp if scoreUp > scoreDown else scoreDown * -1
    return round(final_score * 100, 2)


def get_finnhub_recommendations(stock_symbol):
    finnhub_url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={stock_symbol}&token={finnhub_api_key}"
    response = requests.get(finnhub_url)
    json_response = response.json()
    scores = []
    for recommendation in json_response:
        score = calculate_score(recommendation)
        scores.append({score, recommendation["period"]})
    return scores
