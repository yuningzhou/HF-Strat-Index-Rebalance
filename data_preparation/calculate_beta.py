import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def calculate_russell_beta(price_df, beta_end_date):
    today_index = price_df[price_df['Date'] == beta_end_date].index[0]
    start_index = max(0, today_index - 90)

    price = price_df.iloc[start_index:today_index + 1]
    price['stock'] = price['Open']
    # print(price)

    iwv = pd.read_csv("../data/russell_price/IWV.csv")
    iwv.index = iwv['Date']
    iwv = iwv[price.iloc[0]['Date']:beta_end_date]
    iwv['iwv'] = iwv['Open']
    # print(spy)

    price.index = price['Date']
    price.drop(columns=['Date'], inplace=True)
    iwv.drop(columns=['Date'], inplace=True)

    joined = pd.concat([iwv, price], join='inner', axis=1)
    joined.dropna(inplace=True)
    joined = joined.pct_change()
    joined.dropna(inplace=True)

    beta = np.cov(joined['iwv'], joined['stock'])[0][1] / np.cov(joined['iwv'], joined['stock'])[0][0]
    print(beta)

    return beta


def calculate_sh_beta(price_df, beta_end_date):
    today_index = price_df[price_df['trade_date'] == beta_end_date].index[0]
    start_index = max(0, today_index - 90)

    price = price_df.iloc[start_index:today_index + 1]
    price['stock'] = price['open']
    # print(price)

    etf = pd.read_csv("../data/SH_price/510050.OF.csv")
    etf.index = etf['trade_date']
    etf = etf[price.iloc[0]['trade_date']:beta_end_date]
    etf['etf'] = etf['open']
    # print(spy)

    price.index = price['trade_date']
    price.drop(columns=['trade_date'], inplace=True)
    etf.drop(columns=['trade_date'], inplace=True)

    joined = pd.concat([etf, price], join='inner', axis=1)
    joined.dropna(inplace=True)
    joined = joined.pct_change()
    joined.dropna(inplace=True)
    # print(joined)

    beta = np.cov(joined['etf'], joined['stock'])[0][1] / np.cov(joined['etf'], joined['stock'])[0][0]
    print(beta)

    return beta


if __name__ == '__main__':
    ru_sig = pd.read_csv("../data/cleaned_ru.csv")
    ru_beta = []

    for i in range(len(ru_sig)):
        stock = ru_sig.iloc[i]['code']
        beta_end = ru_sig.iloc[i]['enter_date']
        print(stock + " " + beta_end)
        prices = pd.read_csv("../data/russell_price/" + stock + '.csv')
        ru_beta.append(calculate_russell_beta(prices, beta_end))

    ru_sig['beta'] = ru_beta
    ru_sig.to_csv("../data/cleaned_ru.csv", index=False)

    sh_sig = pd.read_csv("../data/cleaned_SH.csv")
    sh_beta = []
    for i in range(len(sh_sig)):
        stock = sh_sig.iloc[i]['code']
        beta_end = sh_sig.iloc[i]['enter_date']
        print(stock + " " + beta_end)
        prices = pd.read_csv("../data/SH_price/" + stock + '.csv')
        sh_beta.append(calculate_sh_beta(prices, beta_end))
    sh_sig['beta'] = sh_beta

    sh_sig.to_csv("../data/cleaned_SH.csv", index=False)
