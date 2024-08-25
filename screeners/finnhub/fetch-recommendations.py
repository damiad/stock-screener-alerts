import sys
import os
import pandas as pd
from dotenv import load_dotenv

script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.abspath(os.path.join(script_directory, "../../"))
sys.path.append(project_directory)

from utils.utils import safeRequest, print_progress_bar

load_dotenv()
finnhub_api_key = os.getenv("finnhub_api_key")

tickers_file = os.path.join(script_directory, "us_tickers.csv")
recommendations_file = os.path.join(script_directory, "recommendations.csv")


def get_last_processed_symbol():
    if os.path.exists(recommendations_file):
        recommendations_df = pd.read_csv(recommendations_file)
        if not recommendations_df.empty:
            return recommendations_df.iloc[-1]["queriedSymbol"]
    return None


tickers_df = pd.read_csv(tickers_file)
last_symbol = get_last_processed_symbol()
start_collecting = False if last_symbol else True


for index, row in enumerate(tickers_df.itertuples(), start=1):
    if row.type != "Common Stock":
        continue

    symbol = row.symbol

    if not start_collecting:
        if symbol == last_symbol:
            start_collecting = True
        continue

    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={finnhub_api_key}"
    recommendations = safeRequest(url, maxRetries=5, delaySeconds=17)

    print_progress_bar(index + 1, len(tickers_df), prefix="Processing", length=50)

    if recommendations:
        for recommendation in recommendations:
            recommendation_df = pd.DataFrame([recommendation])
            recommendation_df["queriedSymbol"] = symbol
            recommendation_df = recommendation_df[
                [
                    "symbol",
                    "queriedSymbol",
                    "period",
                    "strongBuy",
                    "buy",
                    "hold",
                    "sell",
                    "strongSell",
                ]
            ]
            recommendation_df.to_csv(
                recommendations_file,
                mode="a",
                header=not os.path.exists(recommendations_file),
                index=False,
            )
            # TODO: files could be very large, save it on google drive via googleapiclient
