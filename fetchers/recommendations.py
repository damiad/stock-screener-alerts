from typing import Dict
from enum import Enum
import requests
import os
from dotenv import load_dotenv

load_dotenv()
finnhub_api_key = os.getenv('finnhub_api_key')

class Recommendation:
    json: Dict

    def print_recommendation(self):
        print(self.json)
    def get_score(self):
        pass
    def get_period(self):
        pass 


class FinhubRecommendation(Recommendation):
    def __init__(self, stock_symbol):
        finnhub_url = f'https://finnhub.io/api/v1/stock/recommendation?symbol={stock_symbol}&token={finnhub_api_key}'
        response = requests.get(finnhub_url)
        json_response = response.json()

        self.json = json_response
        self.symbol = stock_symbol 
    def get_score(self):
            recommendation = self.json[0]
            win_strong_weight = 2
            win_weight = 1
            loose_strong_weight = -10
            loose_weight = -5
            loose_neutral_weight = -3
            scoreUp = (recommendation['strongBuy'] * win_strong_weight + recommendation['buy'] * win_weight) / \
                    ((recommendation['strongBuy'] * win_strong_weight + recommendation['buy'] * win_weight) - 
                    (recommendation['strongSell'] * loose_strong_weight + recommendation['sell'] * loose_weight + 
                        recommendation['hold'] * loose_neutral_weight))
            scoreDown = (recommendation['strongSell'] * win_strong_weight + recommendation['sell'] * win_weight) / \
                        ((recommendation['strongSell'] * win_strong_weight + recommendation['sell'] * win_weight) - 
                        (recommendation['strongBuy'] * loose_strong_weight + recommendation['buy'] * loose_weight + 
                        recommendation['hold'] * loose_neutral_weight))
            final_score = scoreUp if scoreUp > scoreDown else scoreDown * -1
            return round(final_score * 100, 2)
    def get_period(self):
        return self.json[0]['period']

    

    



class ZacksRecommendation(Recommendation):
    def __init__(self, stock_symbol):
        zacks_url = f'https://quote-feed.zacks.com/index?t={stock_symbol}'
        response = requests.get(zacks_url)
        json_response = response.json()
        self.json = json_response
        self.symbol = stock_symbol

    def get_score(self):
        #  stock_data = data[symbol]
        data = self.json[self.symbol]
        rank = data['zacks_rank']
        match int(rank):
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
    def get_period(self):
        data = self.json[self.symbol]
        return data['updated']



class AvailableRecommendations(Enum):
    ZACKS = "ZACKS"
    FINHUB = "FINHUB"
    # YAHOO = "YAHOO"


recommendation_dict: Dict[AvailableRecommendations, Recommendation] = {
    AvailableRecommendations.ZACKS: ZacksRecommendation,
    AvailableRecommendations.FINHUB: FinhubRecommendation,
    # AvailableRecommendations.YAHOO: Recommendation()
}



class StockInfo: 
    recommendations: Dict[AvailableRecommendations, Recommendation]
    def __init__(self, symbol:str):
        self.symbol = symbol
        self.recommendations = {}
        for recommendation in AvailableRecommendations:
            self.recommendations[recommendation] = recommendation_dict[recommendation](symbol)



