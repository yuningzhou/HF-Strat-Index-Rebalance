import yfinance as yf
from datetime import datetime


if __name__ == '__main__':

    # sh50 = yf.download("510050.SS", start='2007-06-01', end='2021-06-15')
    # sh50.to_csv("../data/SH_price/sh50.csv")

    spy = yf.download("IWV", start='1995-02-01', end='2021-07-01')
    spy.to_csv("../data/russell_price/IWV.csv")
