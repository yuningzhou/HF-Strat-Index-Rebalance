import tushare
import pandas as pd
from datetime import datetime


if __name__ == '__main__':
    df = pd.read_csv("../data/cleaned_SH.csv")

    token = '0b91b24a09f9ab5f92aeb76f7874b765106831106e524c6b10506a2c'
    pro = tushare.pro_api(token)

    for code in df['code']:
        start_date = "20070601"
        end_date = '20210615'

        date_and_price = pro.daily(ts_code=code, start_date=start_date, end_date=end_date)[
            ["open", "trade_date"]]
        date_and_price['trade_date'] = [datetime.strptime(i, "%Y%m%d") for i in date_and_price['trade_date']]
        date_and_price.index = date_and_price['trade_date']

        date_and_price.drop(columns=['trade_date'], inplace=True)
        date_and_price.to_csv("../data/SH_price/" + code + ".csv")

        print(code + " done")
