import pandas as pd
import os


def get_top_symbols(df, top_n=5):
    symbol_counts = df["symbol"].value_counts()
    return symbol_counts.head(top_n)


def check_subset(symbol_set, queried_symbol_set):
    missing_symbols = symbol_set - queried_symbol_set
    is_subset = len(missing_symbols) == 0

    if not is_subset:
        print("\nSymbols in 'symbol':")
        print(len(symbol_set))
        print("\nSymbols in 'queriedSymbol':")
        print(len(queried_symbol_set))
        print(
            "\nSymbols in 'symbol' that do not have a corresponding match in 'queriedSymbol':"
        )
        print(len(missing_symbols))
        print(missing_symbols)

    return is_subset


def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_directory, "recommendations.csv")

    df = pd.read_csv(csv_file)

    top_5_symbols = get_top_symbols(df, top_n=82)
    print("Top 5 symbols by count:")
    print(top_5_symbols)

    symbol_set = set(df["symbol"])
    queried_symbol_set = set(df["queriedSymbol"])

    is_subset = check_subset(symbol_set, queried_symbol_set)
    print("\nIs 'symbol' a subset of 'queriedSymbol'?:", is_subset)


if __name__ == "__main__":
    main()
