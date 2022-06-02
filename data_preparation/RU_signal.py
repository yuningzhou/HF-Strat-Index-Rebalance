import pandas as pd
from datetime import datetime
import datetime
import yfinance as yf


def stock_in_and_out(a, b):
    in_list = [i for i in a if i not in b]
    out_list = [i for i in b if i not in a]

    in_list = [i for i in in_list if isinstance(i, str)]
    out_list = [i for i in out_list if isinstance(i, str)]

    in_list = [i for i in in_list if i[0].isalpha() == True]
    out_list = [i for i in out_list if i[0].isalpha() == True]

    in_list = [i.split()[0] for i in in_list]
    out_list = [i.split()[0] for i in out_list]

    in_list = [i.split("/")[0] for i in in_list]
    out_list = [i.split("/")[0] for i in out_list]

    in_list = [i for i in in_list if i not in out_list]
    out_list = [i for i in out_list if i not in in_list]
    return [in_list, out_list]


def first_friday_in_may(year):
    fir_fri = datetime.date(year, 5, 1)
    w = fir_fri.weekday()
    if w != 4:
        fir_fri = fir_fri.replace(day=(1 + (4 - w) % 7))
    return fir_fri


def last_friday_in_june(year):
    last_fri = datetime.date(year, 6, 30)
    w = last_fri.weekday()
    if w != 4:
        last_fri = last_fri.replace(day=(30 - (w - 4) % 7))
    return last_fri


if __name__ == '__main__':

    ru_3000 = pd.read_excel("../data/russell_index_change.xlsx")

    ###################

    Stock_Code = []
    Rank_day = []
    In_and_out = []
    Enter_day = []
    Close_day = []
    Enter_price = []
    Close_price = []

    for i in range(len(ru_3000.columns) - 1):

        year = int(ru_3000.columns[i])
        rank_date = first_friday_in_may(year)
        enter_date = rank_date + datetime.timedelta(days=3)
        close_date = last_friday_in_june(year) + datetime.timedelta(days=3)
        in_and_out_list = stock_in_and_out(list(ru_3000.iloc[:, i]), list(ru_3000.iloc[:, i + 1]))
        in_list = in_and_out_list[0]
        out_list = in_and_out_list[1]
        # combined_list = in_list + out_list

        print("############ YEAR " + str(year) + " ############")
        print("Enter date for this year: " + str(enter_date))
        print("Closing date for this year: " + str(close_date))
        print("Trading " + str(len(in_list) + len(out_list)) + " stocks this year")

        for j in in_list:
            Stock_Code.append(j)
            Rank_day.append(rank_date)
            In_and_out.append(1)
            Enter_day.append(enter_date)
            Close_day.append(close_date)
            try:
                Enter_price.append(
                    yf.download(j, start=enter_date, end=enter_date + datetime.timedelta(days=1), progress=True)[
                        "Open"].iloc[0])
            except:
                Enter_price.append("NA")

            try:
                Close_price.append(
                    yf.download(j, start=close_date, end=close_date + datetime.timedelta(days=1), progress=True)[
                        "Open"].iloc[0])
            except:
                Close_price.append("NA")

        for j in out_list:
            Stock_Code.append(j)
            Rank_day.append(rank_date)
            In_and_out.append(0)
            Enter_day.append(enter_date)
            Close_day.append(close_date)
            try:
                Enter_price.append(
                    yf.download(j, start=enter_date, end=enter_date + datetime.timedelta(days=1), progress=True)[
                        "Open"].iloc[0])
            except:
                Enter_price.append("NA")

            try:
                Close_price.append(
                    yf.download(j, start=close_date, end=close_date + datetime.timedelta(days=1), progress=True)[
                        "Open"].iloc[0])
            except:
                Close_price.append("NA")

        print("############ Done with " + str(year) + " ############")
        print("")

        output = pd.DataFrame([Rank_day, Stock_Code, In_and_out, Enter_day, Enter_price, Close_day, Close_price])
        output = output.transpose()
        output.set_axis(["dates", "code", "in/out", "enter_date", "enter_price", "close_date", "close_price"], axis=1,
                        inplace=True)
        output.set_index("dates", inplace=True)
        output.dropna(inplace=True)
        output.to_csv("../data/russell.csv", index=True)
