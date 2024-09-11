import pandas as pd
import os


def meets_criteria(latest_period):
    if "." in latest_period["symbol"]:
        return False
    total_ratings = (
        latest_period["strongBuy"]
        + latest_period["buy"]
        + latest_period["hold"]
        + latest_period["sell"]
        + latest_period["strongSell"]
    )

    if (
        total_ratings >= 20
        and latest_period["sell"] == 0
        and latest_period["strongSell"] == 0
    ):
        hold_percentage = latest_period["hold"] / total_ratings
        if hold_percentage < 0.1:
            return True

    return False


def arrange_symbols(filtered_symbols):
    for symbol_data in filtered_symbols:
        total_ratings = (
            symbol_data["strongBuy"]
            + symbol_data["buy"]
            + symbol_data["hold"]
            + symbol_data["sell"]
            + symbol_data["strongSell"]
        )
        symbol_data["hold_percentage"] = symbol_data["hold"] / total_ratings * 100
        symbol_data["strongBuy_percentage"] = symbol_data["strongBuy"] / total_ratings * 100

    return sorted(filtered_symbols, key=lambda x: x["hold_percentage"], reverse=False)


def process_symbols(df):
    result = []

    # Create a map of symbols to their period data
    symbol_period_map = {}

    for _, row in df.iterrows():
        symbol = row["symbol"]

        if symbol not in symbol_period_map:
            symbol_period_map[symbol] = []

        symbol_period_map[symbol].append(row)

    # Process each symbol
    for symbol, periods in symbol_period_map.items():
        # Sort periods in descending order to get the latest one
        periods.sort(key=lambda x: x["period"], reverse=True)
        latest_period = periods[0]

        if meets_criteria(latest_period):
            result.append(
                {
                    "symbol": symbol,
                    "period": latest_period["period"],
                    "strongBuy": latest_period["strongBuy"],
                    "buy": latest_period["buy"],
                    "hold": latest_period["hold"],
                    "sell": latest_period["sell"],
                    "strongSell": latest_period["strongSell"],
                }
            )
    arranged_results = arrange_symbols(result)
    return arranged_results


def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_directory, "recommendations.csv")
    output_file = os.path.join(script_directory, "most-recommended.csv")
    df = pd.read_csv(csv_file)

    filtered_symbols = process_symbols(df)

    if filtered_symbols:
        result_df = pd.DataFrame(filtered_symbols)
        result_df.to_csv(output_file, index=False)
        print(f"Filtered symbols saved to {output_file}")
    else:
        print("No symbols met the criteria")


if __name__ == "__main__":
    main()
