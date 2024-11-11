import sys
import time
import requests
import json
import sys
import os
import math

class TickerData:
    def __init__(self, ticker, prices):
        self.ticker = ticker
        self.prices = prices

# Takes a ticker and an API key and gets the 100 day price history from AlphaVantage. Returns JSON dictionary.
def get_live_ticker_data(ticker: str, api_key: str) -> any:
    print("Calling AlphaVantage for ticker: ", ticker)
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker.upper() + "&apikey=" + api_key
    response = requests.get(url)
    time.sleep(1)
    if response.status_code != 200:
        print("FATAL: Bad HTTP code: ", response.status_code)
        exit()
    if "Time Series (Daily)" not in response.json():
        print("FATAL: API Failure")
        print(response.json())
        exit()
    return response.json()

def process_ticker_json(ticker: str, ticker_json: any) -> TickerData:
    time_series = ticker_json["Time Series (Daily)"]
    prices = []
    for date in time_series:
        prices.append(float(time_series[date]["4. close"]))
    return TickerData(ticker, prices)

# Receives a ticker and live json data and writes the data to a file.
# The file will always be the lower case ticker suffixed with ".json". This format is important as it will be how the
# offline data reader finds the offline files later.
def write_ticker_data(ticker: str, json_data: str):
    filename: str = ticker.lower() + ".json"
    with open(filename, 'w') as f:
        json.dump(json_data, f)

def read_offline_ticker_data(ticker: str) -> TickerData:
    filename: str = ticker.lower() + ".json"
    if not os.path.exists(filename):
        print("FATAL: Offline data not found for ", ticker)
        exit()
    with open(filename, 'r') as file:
        return process_ticker_json(ticker, json.load(file))

def generate_empty_matrix(tickers: list) -> dict:
    matrix = {}
    for ticker_i in tickers:
        matrix[ticker_i] = {}
        for ticker_j in tickers:
            matrix[ticker_i][ticker_j] = None
    return matrix

def calculate_correlation(x: list, y: list) -> float:
    x_bar = sum(x) / len(x)
    y_bar = sum(y) / len(y)

    var_x = sum((x_i - x_bar) ** 2 for x_i in x)
    var_y = sum((y_i - y_bar) ** 2 for y_i in y)

    assert len(x) == len(y)
    numerator = sum((x_i - x_bar) * (y_i - y_bar) for x_i, y_i in zip(x, y))
    denominator = math.sqrt(var_x * var_y)
    return numerator / denominator

def generate_correlations(ticker_data_map: dict) -> dict:
    matrix = generate_empty_matrix(list(ticker_data_map.keys()))
    for ticker_i in matrix.keys():
        for ticker_j in matrix[ticker_i].keys():
            ticker_i_data = ticker_data_map[ticker_i]
            ticker_j_data = ticker_data_map[ticker_j]
            correlation = calculate_correlation(ticker_i_data.prices, ticker_j_data.prices)
            matrix[ticker_i][ticker_j] = correlation
    return matrix


def print_correlations(matrix: dict) -> None:
    # Create ticker strings, all tickers must be the same length for readability.
    ticker_strings = {}
    ticker_string_size = 20
    ticker_strings_list = []
    for ticker_i in matrix.keys():
        ticker_string = ticker_i + " "*(ticker_string_size - len(ticker_i))
        ticker_strings[ticker_i] = ticker_string
        ticker_strings_list.append(ticker_string)
    # Build matrix string represntation and print it.
    print(" "*ticker_string_size + "".join(ticker_strings_list))
    for ticker_i in matrix.keys():
        curr_str = ticker_strings[ticker_i]
        for ticker_j in matrix[ticker_i].keys():
            str_val = str(round(matrix[ticker_i][ticker_j], 4))
            str_val_len = len(str_val)
            curr_str += str_val + " "*(ticker_string_size - str_val_len)
        print(curr_str)

def print_help():
    print("usage: python main.py <apikey> <runmode> <ticker1> <ticker2> ...")
    print("apikey: an AlphaVantage API key (free is limited to 25 calls per day)")
    print("runmode: Mode that the tool will run in. possible values:")
    print("  live: Gathers data from AlphaVantage and run correlation analysis on it.")
    print("  offline: Reads offline data from current directory, file names must be lowercase ticker.")
    print("  sample: Reads live ticker data from AlphaVantage and saves to current directory.")
    exit()

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) < 5 or "help" in arguments: print_help()
    api_key: str = arguments[1]
    runmode: str = arguments[2]
    tickers: list[str] = arguments[3:]

    # Gather data from AlphaVantage and perform correlation, data will not be stored.
    if runmode == "live":
        print("Running correlation using data from AlphaVantage...")
        for ticker in tickers:
            ticker_json = get_live_ticker_data(ticker, api_key)
            write_ticker_data(ticker, ticker_json)
        ticker_data = {}
        for ticker in tickers:
            data: TickerData = read_offline_ticker_data(ticker)
            ticker_data[ticker] = data
        correlations = generate_correlations(ticker_data)
        print_correlations(correlations)

    # Perform correlation analysis on offline data.
    elif runmode == "offline":
        print("Running correlation using offline data...")
        ticker_data = {}
        for ticker in tickers:
            data: TickerData = read_offline_ticker_data(ticker)
            ticker_data[ticker] = data
        correlations = generate_correlations(ticker_data)
        print_correlations(correlations)
    # Gather JSON data from the given stocks and save them to the hard drive.
    elif runmode == "sample":
        print("Gathering offline data...")
        for ticker in tickers:
            ticker_json = get_live_ticker_data(ticker, api_key)
            write_ticker_data(ticker, ticker_json)

    else: print_help()
