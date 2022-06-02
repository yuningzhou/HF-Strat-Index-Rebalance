import pandas as pd


if __name__ == '__main__':
    SH = pd.read_csv("../data/cleaned_SH.csv")
    SH = SH[::-1]
    SH.reset_index(inplace=True)
    SH.drop(columns=['index'], inplace=True)
    SH.dropna(inplace=True)
    SH['year'] = [i[:4] for i in SH['rank dates']]
    SH = SH[['rank dates', 'year', 'code', 'in/out', 'enter_date', 'exit_date', 'beta']]
    SH['enter_date'] = [str(i)[:10] for i in SH['enter_date']]
    SH['exit_date'] = [str(i)[:10] for i in SH['exit_date']]

    SH_in_the_sample = SH[SH['year'].astype(int) < 2018]
    SH_out_of_sample = SH[SH['year'].astype(int) >= 2018]

    SH_in_the_sample.to_csv("../data/SH_signal_its.csv")
    SH_out_of_sample.to_csv("../data/SH_signal_oos.csv")

    RU = pd.read_csv("../data/cleaned_RU.csv")
    RU = RU[::-1]
    RU.reset_index(inplace=True)
    RU.drop(columns=['index'], inplace=True)
    RU.dropna(inplace=True)
    RU['year'] = [i[:4] for i in RU['dates']]
    RU = RU[['dates', 'year', 'code', 'in/out', 'enter_date', 'close_date', 'beta']]

    RU_in_the_sample = RU[RU['year'].astype(int) < 2015]
    RU_out_of_sample = RU[RU['year'].astype(int) >= 2015]

    RU_in_the_sample.to_csv("../data/RU_signal_its.csv")
    RU_out_of_sample.to_csv("../data/RU_signal_oos.csv")
