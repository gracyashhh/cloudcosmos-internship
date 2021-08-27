import yfinance as yf

import matplotlib.pyplot as plt
df = yf.download("TSLA", start="2021-06-01", end="2021-08-22", interval="1d")
print(df.head())
t = yf.Ticker("T")
print(t.dividends)
t.dividends.plot(figsize=(14, 7))
plt.show()