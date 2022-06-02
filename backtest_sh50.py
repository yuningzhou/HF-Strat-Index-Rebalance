import pandas as pd
import strat.sh50 as sh
import matplotlib.pyplot as plt


if __name__ == '__main__':
    signal_file = pd.read_csv('data/SH_signal_its.csv')
    price_files = 'data/SH_price/'

    bank_rate = pd.read_excel("data/bank_ir.xlsx")['1-year interest rate'].mean()*0.01

    print("#############Backtesting: Beta Hedge + Shorting Available#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=False,
                      beta_hedge=True, can_short=True)
    df_1 = backtest.account
    df_1.to_csv("backtest_results/SH_50_basic_betahedged.csv")

    print("#############Backtesting: Beta Hedge + Shorting Available + Stop Loss#############")
    backtest = sh.SH50(signal=signal_file,  price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=False,
                      beta_hedge=True, can_short=True)
    df_2 = backtest.account
    df_2.to_csv("backtest_results/SH_50_sl_betahedged.csv")

    print("#############Backtesting: Beta Hedge + Shorting Available + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=True,
                      beta_hedge=True, can_short=True)
    df_3 = backtest.account
    df_3.to_csv("backtest_results/SH_50_bank_betahedged.csv")

    print("#############Backtesting: Beta Hedge + Shorting Available + Stop Loss + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=True,
                      beta_hedge=True, can_short=True)
    df_4 = backtest.account
    df_4.to_csv("backtest_results/SH_50_sl_bank_betahedged.csv")

    print("#############Backtesting: Beta Hedge + NO Shorting#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=False,
                      beta_hedge=True, can_short=False)
    df_5 = backtest.account
    df_5.to_csv("backtest_results/SH_50_noshort_basic_betahedged.csv")

    print("#############Backtesting: Beta Hedge + NO Shorting + Stop Loss#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=False,
                      beta_hedge=True, can_short=False)
    df_6 = backtest.account
    df_6.to_csv("backtest_results/SH_50_noshort_sl_betahedged.csv")

    print("#############Backtesting: Beta Hedge + NO Shorting + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=True,
                      beta_hedge=True, can_short=False)
    df_7 = backtest.account
    df_7.to_csv("backtest_results/SH_50_noshort_bank_betahedged.csv")

    print("#############Backtesting: Beta Hedge + NO Shorting + Stop Loss + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=True,
                      beta_hedge=True, can_short=False)
    df_8 = backtest.account
    df_8.to_csv("backtest_results/SH_50_noshort_sl_bank_betahedged.csv")

    # plt.figure(figsize=(15, 10))
    # plt.plot(df_1['NAV'], label='basic')
    # plt.plot(df_2['NAV'], label='stop loss')
    # plt.plot(df_3['NAV'], label='store in bank')
    # plt.plot(df_4['NAV'], label='stop loss + store in bank')
    # plt.plot(df_5['NAV'], label='shorting not allowed basic')
    # plt.plot(df_6['NAV'], label='shorting not allowed with stop loss')
    # plt.plot(df_7['NAV'], label='shorting not allowed but store in bank')
    # plt.plot(df_8['NAV'], label='shorting not allowed with stop loss + store in bank')
    # plt.legend()
    # plt.gca().xaxis.set_major_locator(plt.MultipleLocator(300))
    # plt.show()
    # #

    print("#############Backtesting: NO Beta Hedge + Shorting Available#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=False,
                      beta_hedge=False, can_short=True)
    df_9 = backtest.account
    df_9.to_csv("backtest_results/SH_50_basic_nobetahedged.csv")
    print("########################Done!########################")
    print("")

    print("#############Backtesting: NO Beta Hedge + Shorting Available + Stop Loss#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=False,
                      beta_hedge=False, can_short=True)
    df_10 = backtest.account
    df_10.to_csv("backtest_results/SH_50_sl_nobetahedged.csv")
    print("########################Done!########################")
    print("")

    print("#############Backtesting: NO Beta Hedge + Shorting Available + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=True,
                      beta_hedge=False, can_short=True)
    df_11 = backtest.account
    df_11.to_csv("backtest_results/SH_50_bank_nobetahedged.csv")
    print("########################Done!########################")
    print("")

    print("#############Backtesting: NO Beta Hedge + + Shorting Available + "
          "Stop Loss + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=True,
                      beta_hedge=False, can_short=True)
    df_12 = backtest.account
    df_12.to_csv("backtest_results/SH_50_sl_bank_nobetahedged.csv")
    print("########################Done!########################")
    print("")

    print("#############Backtesting: NO Beta Hedge + NO Shorting#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=False,
                      beta_hedge=False, can_short=False)
    df_13 = backtest.account
    df_13.to_csv("backtest_results/SH_50_noshort_basic_nobetahedged.csv")
    print("########################Done!########################")
    print("")

    print("#############Backtesting: NO Beta Hedge + NO Shorting + Stop Loss#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=False,
                      beta_hedge=False, can_short=False)
    df_14 = backtest.account
    df_14.to_csv("backtest_results/SH_50_noshort_sl_nobetahedged.csv")
    print("########################Done!########################")
    print("")

    print("#############Backtesting: NO Beta Hedge + NO Shorting + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=False, store_in_bank=True,
                      beta_hedge=False, can_short=False)
    df_15 = backtest.account
    df_15.to_csv("backtest_results/SH_50_noshort_bank_nobetahedged.csv")
    print("########################Done!########################")
    print("")

    print("#############Backtesting: NO Beta Hedge + NO Shorting + Stop Loss + Capital Optimization#############")
    backtest = sh.SH50(signal=signal_file, price_data_path=price_files, investment=10000000, rate=bank_rate)
    backtest.backtest(2007, 12, 10, 3656, verbose=True, stop_loss=True, store_in_bank=True,
                      beta_hedge=False, can_short=False)
    df_16 = backtest.account
    df_16.to_csv("backtest_results/SH_50_noshort_sl_bank_nobetahedged.csv")
    print("########################Done!########################")
    print("")
    #
    # plt.figure(figsize=(15, 10))
    # plt.plot(df_8['NAV'], label='basic')
    # plt.plot(df_9['NAV'], label='stop loss')
    # plt.plot(df_10['NAV'], label='store in bank')
    # plt.plot(df_11['NAV'], label='stop loss + store in bank')
    # plt.plot(df_12['NAV'], label='shorting not allowed basic')
    # plt.plot(df_13['NAV'], label='shorting not allowed with stop loss')
    # plt.plot(df_14['NAV'], label='shorting not allowed but store in bank')
    # plt.plot(df_15['NAV'], label='shorting not allowed with stop loss + store in bank')
    # plt.legend()
    # plt.gca().xaxis.set_major_locator(plt.MultipleLocator(300))
    # plt.show()
