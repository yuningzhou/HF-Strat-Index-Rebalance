import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import tushare

if __name__ == '__main__':
    SH_50 = pd.read_csv("/Users/baoyechen/Desktop/Hedge Funds.nosync/MATHGR5300-Hedge-Funds-Strat-Risk/"
                        "Index-Rebalance/data/SH_50.csv")
    SH_50 = pd.DataFrame([SH_50["rank dates"], SH_50["rebalance dates"], SH_50["code"], SH_50["in/out"]])
    SH_50 = SH_50.transpose()
    SH_50["rebalance dates"] = pd.to_datetime(SH_50["rebalance dates"], dayfirst=False)  # transfer it into timestamp
    SH_50["rank dates"] = pd.to_datetime(SH_50["rank dates"], dayfirst=False)  # transfer it into timestamp
    SH_50.set_index("rank dates", inplace=True)  # set the date as the index.
    token = '0b91b24a09f9ab5f92aeb76f7874b765106831106e524c6b10506a2c'
    pro = tushare.pro_api(token)
    enter_date = []
    exit_date = []
    enter_price = []
    exit_price = []

    for i in range(len(SH_50)):
        start_date = SH_50.index[i] + timedelta(days=1)
        end_date = SH_50.iloc[i]["rebalance dates"] + timedelta(days=1)
        code = SH_50.iloc[i]["code"]
        start_date_string = start_date.strftime("%Y%m%d")
        end_date_string = end_date.strftime("%Y%m%d")
        date_and_price = pro.daily(ts_code=code, start_date=start_date_string, end_date=end_date_string)[
            ["open", "trade_date"]]
        date_and_price['trade_date'] = [datetime.strptime(i, "%Y%m%d") for i in date_and_price['trade_date']]
        if len(date_and_price) > 0:
            price_2 = date_and_price.iloc[0]["open"]
            date_2 = date_and_price.iloc[0]["trade_date"]
            price_1 = date_and_price.iloc[-1]["open"]
            date_1 = date_and_price.iloc[-1]["trade_date"]
            enter_date.append(date_1)
            exit_date.append(date_2)
            enter_price.append(price_1)
            exit_price.append(price_2)
        else:
            enter_date.append("NA")
            exit_date.append("NA")
            enter_price.append("NA")
            exit_price.append("NA")

        print(code + "done")

    SH_50["enter_date"] = enter_date
    SH_50["enter_price"] = enter_price
    SH_50["exit_date"] = exit_date
    SH_50["exit_price"] = exit_price

    SH_50.to_csv("/Users/baoyechen/Desktop/Hedge Funds.nosync/MATHGR5300-Hedge-Funds-Strat-Risk/"
                 "Index-Rebalance/data/cleaned_SH.csv")
