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

Offline data that is more than 1 day old will not produce accurate correlations.

### Example Call
```shell
PS C:\Users\matts\stock_correlations> python main.py randomapikey live nke teck czr amd
Running correlation using data from AlphaVantage...
Offline data available for nke
Offline data available for teck
Calling AlphaVantage for ticker:  czr
Offline data available for amd
                    nke                 teck                czr                 amd
nke                 1.0                 -0.6765             0.5116              -0.1873
teck                -0.6765             1.0                 -0.5269             0.4059
czr                 0.5116              -0.5269             1.0                 -0.3383
amd                 -0.1873             0.4059              -0.3383             1.0
PS C:\Users\matts\stock_correlations>
```