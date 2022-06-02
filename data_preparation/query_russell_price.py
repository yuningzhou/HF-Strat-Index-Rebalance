import pandas as pd
import yfinance as yf


if __name__ == '__main__':

    signal = pd.read_csv("../data/cleaned_RU.csv")

    for i, ticker in enumerate(signal['code']):
        try:
            df = yf.download(ticker, start='1995-02-01', end='2021-07-01')
            df.to_csv("../data/russell_price/" + ticker + ".csv")
            print(ticker + " done, " + str(i) + "/" + str(len(signal['code'])))
        except:
            print(ticker + " failed")
