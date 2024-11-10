# Stock Correlation Tool

Calculates the correlation coefficients between the price movements of a set of stocks.

## Requirements

- [An AlphaVantage free or paid API key](https://www.activestate.com/resources/quick-reads/how-to-pip-install-requests-python-package/)
- [Python3 installed](https://www.python.org/downloads/)
- [Python requests library](https://www.activestate.com/resources/quick-reads/how-to-pip-install-requests-python-package/)

## Usage

The correlation tool has two main modes that it can be used in. The purpose of these modes is to reduce the number of
calls to the AlphaVantage API

### Live Mode

This mode gathers live data from AlphaVantage and runs the correlation algorithm.

### Offline Mode

This mode includes two steps: gathering the data and correlating.

- Gathering offline data: `python main.py <api key> sample <ticker1> <ticker2> ...`
- Running correlation: `python main.py <api key> offline <ticker1> <ticker2> ...`
