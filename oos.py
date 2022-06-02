import pandas as pd
import strat.sh50 as sh
import strat.russell3000 as ru
import matplotlib.pyplot as plt

if __name__ == '__main__':
    sh_signal_file = pd.read_csv('data/SH_signal_oos.csv')
    sh_price_files = 'data/SH_price/'
    sh_bank_rate = pd.read_excel("data/bank_ir.xlsx")['1-year interest rate'].mean() * 0.01

    print("#############Backtesting: Beta Hedge + Shorting Available + Capital Optimization#############")
    backtest = sh.SH50(signal=sh_signal_file, price_data_path=sh_price_files, investment=10000000, rate=sh_bank_rate)
    backtest.backtest(2018, 5, 28, 1116, verbose=True, stop_loss=False, store_in_bank=True,
                      beta_hedge=True, can_short=True)
    df_1 = backtest.account
    df_1.to_csv("backtest_results/SH_50_OOS.csv")
    #
    # plt.figure(figsize=(15, 10))
    # plt.plot(df_1['NAV'], label='SH_OOS')
    # plt.gca().xaxis.set_major_locator(plt.MultipleLocator(300))
    # plt.show()

    ru_signal_file = pd.read_csv('data/RU_signal_oos.csv')
    ru_price_files = 'data/russell_price/'
    ru_bank_rate = 0.03

    print("#############Backtesting: Beta Hedge + Shorting Available + Capital Optimization#############")
    backtest = ru.Russell3000(signal=ru_signal_file, price_data_path=ru_price_files,
                              investment=10000000, rate=ru_bank_rate)
    backtest.backtest(2015, 5, 1, 2251, verbose=True, stop_loss=False, store_in_bank=True, beta_hedge=True)
    df_2 = backtest.account
    df_2.to_csv("backtest_results/RU_3000_OOS.csv")
    #
    # plt.figure(figsize=(15, 10))
    # plt.plot(df_2['NAV'], label='RU_OOS')
    # plt.gca().xaxis.set_major_locator(plt.MultipleLocator(300))
    # plt.legend()
    # plt.show()
