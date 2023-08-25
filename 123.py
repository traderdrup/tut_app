import yfinance as yf

stock = yf.Ticker('GN.CO').history(start = '2022-08-24', end = '2023-08-24')
print(stock.count())