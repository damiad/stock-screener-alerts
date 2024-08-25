import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
finnhub_api_key = os.getenv("finnhub_api_key")
url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={finnhub_api_key}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_directory, "us_tickers.csv")
    df.to_csv(output_file, index=False)
    print(f"Data saved to '{output_file}'")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
