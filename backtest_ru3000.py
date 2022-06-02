import pandas as pd
import strat.russell3000 as ru
import matplotlib.pyplot as plt


if __name__ == '__main__':
    signal_file = pd.read_csv('data/RU_signal_its.csv')
    price_files = 'data/russell_price/'

    bank_rate = 0.03

    # backtest = ru.Russell3000(signal=signal_file, price_data_path=price_files, investment=10000000, rate=0.02)
    # backtest.backtest(2001, 5, 4, 4806, verbose=True, stop_loss=False, store_in_bank=False, beta_hedge=True)
    # df_1 = backtest.account
    # df_1.to_csv("backtest_results/RU_3000_basic.csv")

    print("#############Backtesting: Beta Hedge + Shorting Available#############")
    backtest = ru.Russell3000(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2001, 5, 4, 4806, verbose=True, stop_loss=False, store_in_bank=False,
                      beta_hedge=True)
    df_1 = backtest.account
    df_1.to_csv("backtest_results/RU_3000_basic_betahedged.csv")

    print("#############Backtesting: Beta Hedge + Shorting Available + Stop Loss#############")
    backtest = ru.Russell3000(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2001, 5, 4, 4806, verbose=True, stop_loss=True, store_in_bank=False,
                      beta_hedge=True)
    df_2 = backtest.account
    df_2.to_csv("backtest_results/RU_3000_sl_betahedged.csv")

    print("#############Backtesting: Beta Hedge + Shorting Available + Capital Optimization#############")
    backtest = ru.Russell3000(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2001, 5, 4, 4806, verbose=True, stop_loss=False, store_in_bank=True,
                      beta_hedge=True)
    df_3 = backtest.account
    df_3.to_csv("backtest_results/RU_3000_bank_betahedged.csv")

    print("#############Backtesting: Beta Hedge + Shorting Available + Stop Loss + Capital Optimization#############")
    backtest = ru.Russell3000(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2001, 5, 4, 4806, verbose=True, stop_loss=True, store_in_bank=True,
                      beta_hedge=True)
    df_4 = backtest.account
    df_4.to_csv("backtest_results/RU_3000_sl_bank_betahedged.csv")

    plt.figure(figsize=(15, 10))
    plt.plot(df_1['NAV'], label='basic')
    plt.plot(df_2['NAV'], label='stop loss')
    plt.plot(df_3['NAV'], label='store in bank')
    plt.plot(df_4['NAV'], label='stop loss + store in bank')
    plt.legend()
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(300))
    plt.show()
