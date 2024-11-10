import sys
import time
import requests, json, sys

class TickerData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.prices = []

# Takes a ticker and an API key and gets the 100 day price history from AlphaVantage. Returns JSON dictionary.
def get_live_ticker_data(ticker: str, api_key: str) -> any:
    print("Calling AlphaVantage for ticker: ", ticker)
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + ticker.upper() + "&apikey=" + api_key
    response = requests.get(url)
    time.sleep(1)
    if response.status_code != 200 or "Time Series (Daily)" not in response.json():
        print("Bad HTTP code: ", response.status_code)
        exit()
    if "Time Series (Daily)" not in response.json():
        print("API Failure")
        exit()
    return response.json()

def process_ticker_json(ticker_json: any) -> TickerData:
    pass

# Receives a ticker and live json data and writes the data to a file.
# The file will always be the lower case ticker suffixed with ".json". This format is important as it will be how the
# offline data reader finds the offline files later.
def write_ticker_data(ticker: str, json_data: str):
    filename: str = ticker.lower() + ".json"
    with open(filename, 'w') as f:
        json.dump(json_data, f)

def read_ticker_data(ticker: str) -> TickerData:
    pass

def correlation(ticker1: TickerData, ticker2: TickerData) -> float:
    pass

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
    # Perform correlation analysis on offline data.
    elif runmode == "offline":
        print("Running correlation using offline data...")
        pass
    # Gather JSON data from the given stocks and save them to the hard drive.
    elif runmode == "sample":
        print("Gathering offline data...")
        for ticker in tickers:
            ticker_json = get_live_ticker_data(ticker, api_key)
            write_ticker_data(ticker, ticker_json)
    else: print_help()
