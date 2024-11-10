import sys

class TickerData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.prices = []

def get_live_ticker_data(ticker: str, api_key: str) -> TickerData:
    pass

# Debug functions ----

def write_ticker_data(ticker_data: TickerData):
    pass

def read_ticker_data(ticker: str) -> TickerData:
    pass

# End Debug functions -----

def correlation(ticker1: TickerData, ticker2: TickerData) -> float:
    pass

def print_help():
    print("usage: python main.py <apikey> <runmode> <ticker1> <ticker2> ...")
    print("apikey: an AlphaVantage API key (free is limited to 25 calls per day)")
    print("runmode: Mode that the tool will run in. possible values:")
    print("  live: Gathers data from AlphaVantage and run correlation analysis on it.")
    print("  offline: Reads offline data from current directory, file names must be lowercase ticker.")
    print("  sample: Reads live ticker data from AlphaVantage and saves to current directory.")

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) < 5 or "help" in arguments: print_help()
    api_key: str = arguments[1]
    runmode: str = arguments[2]
    tickers: list[str] = arguments[3:]
    if runmode == "live":
        print("Running correlation using data from AlphaVantage...")
    elif runmode == "offline":
        print("Running correlation using offline data...")
        pass
    elif runmode == "sample":
        print("Gathering offline data from AlphaVantage...")
        pass
    else: print_help()
