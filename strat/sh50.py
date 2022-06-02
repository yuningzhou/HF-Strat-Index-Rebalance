import pandas as pd
import datetime as d


class SH50:
    """
    The class for SSE 50 strategy
    """

    def __init__(self, signal, price_data_path, investment, rate):

        self.signal = signal
        self.price_data_path = price_data_path

        self.book = {}                                      # a dictionary to store the current positions
        self.need_to_trade = {}                             # a dictionary to store the stocks that we need to trade
        self.cash_position = investment
        self.notionals = 0
        self.long_notionals = 0
        self.short_notionals = 0
        self.hedge_position = 0
        self.hedge_notional = 0
        self.nav = self.cash_position + self.notionals

        self.bank_rate = rate
        self.transaction_cost = 0.00051
        self.security_financing_cost = 0.0003

        self.account = None

    def create_backtest_df(self, start_y, start_m, start_d, num_of_days):
        """
        Function to initiate an empty dataframe to store daily results
        """

        start = d.date(start_y, start_m, start_d)
        date_list = [(start + d.timedelta(days=day)).isoformat() for day in range(num_of_days)]

        self.account = pd.DataFrame(index=date_list, columns=['cash', 'notionals', 'fee_incurred', 'hedge_notional',
                                                              'hedge_position', 'long_notionals', 'short_notionals',
                                                              'NAV'])

    def book_beta(self, date, current_index):
        """
        Function to calculate the total beta of a given portfolio
        """
        position_list = []
        beta_list = []
        for stock in list(self.book.keys()):
            prices = pd.read_csv(self.price_data_path + stock + '.csv')
            price = prices[prices['trade_date'] == date]['open']

            # if no price data found for a certain day, roll back until the closest day that we can find a price
            k = 1
            while len(price) == 0:
                price = prices[prices['trade_date'] == self.account.index[current_index - k]]['open']
                k += 1
            price = float(price)
            position_list.append(self.book[stock][0] * price)
            beta_list.append(self.book[stock][2])

        total_beta_notional = sum([beta_list[i] * position_list[i] for i in range(len(beta_list))])
        total_position = sum([abs(i) for i in position_list])
        # print(total_position)
        return total_beta_notional / total_position

    def backtest(self, start_y, start_m, start_d, num_of_days, verbose=False,
                 stop_loss=False, store_in_bank=False, can_short=True, beta_hedge=False):
        self.create_backtest_df(start_y, start_m, start_d, num_of_days)

        if store_in_bank:
            print("when no position, will store money in bank to earn annualized interest of: " + str(self.bank_rate))

        enter_dates = self.signal['enter_date'].unique()
        exit_dates = self.signal['exit_date'].unique()
        rank_dates = self.signal['rank dates'].unique()

        for j, i in enumerate(self.account.index):

            fee = 0

            # update account values

            self.notionals = 0
            self.long_notionals = 0
            self.short_notionals = 0

            for stock in list(self.book):
                prices = pd.read_csv(self.price_data_path + stock + '.csv')
                price = prices[prices['trade_date'] == i]['open']

                # if no price data found for a certain day, roll back until the closest day that we can find a price
                k = 1
                while len(price) == 0:
                    price = prices[prices['trade_date'] == self.account.index[j - k]]['open']
                    k += 1
                price = float(price)

                self.notionals += self.book[stock][0] * price
                if self.book[stock][0] > 0:
                    self.long_notionals += self.book[stock][0] * price
                else:
                    self.short_notionals += self.book[stock][0] * price

            if beta_hedge and len(self.book) != 0:
                etf_prices = pd.read_csv(self.price_data_path + "510050.OF.csv")
                etf_price = etf_prices[etf_prices['trade_date'] == i]['open']
                k = 1
                while len(etf_price) == 0:
                    etf_price = etf_prices[etf_prices['trade_date'] == self.account.index[j - k]]['open']
                    k += 1
                self.hedge_notional = self.hedge_position * float(etf_price)

            fee += abs(self.short_notionals) * self.security_financing_cost

            # if it is a rank date, perform the portfolio weighting
            if i in rank_dates:
                stocks = self.signal[self.signal['rank dates'] == i]

                long = stocks[stocks['in/out'] == 1]
                long.index = long['code']
                long_weighting = 1 / len(long) if len(long) != 0 else 0

                if can_short:
                    long_notional = self.cash_position * 0.5 * long_weighting
                else:
                    long_notional = self.cash_position * long_weighting
                for stock in long.index:
                    self.need_to_trade[stock] = [long_notional, long.loc[stock]['enter_date'],
                                                 long.loc[stock]['exit_date'], long.loc[stock]['beta']]

                if can_short:
                    short = stocks[stocks['in/out'] == 0]
                    short.index = short['code']
                    short_weighting = 1 / len(short) if len(short) != 0 else 0
                    short_notional = -self.cash_position * 0.5 * short_weighting
                    for stock in short.index:
                        self.need_to_trade[stock] = [short_notional, short.loc[stock]['enter_date'],
                                                     short.loc[stock]['exit_date'], short.loc[stock]['beta']]

                if verbose:
                    print(i + ", a rank date. Signal Generated.")
                    print("need to trade")
                    print(self.need_to_trade)
                    print("")

            # If it is enter date, enter the positions
            if i in enter_dates:

                for stock in list(self.need_to_trade):
                    if self.need_to_trade[stock][1] == i:
                        prices = pd.read_csv(self.price_data_path + stock + '.csv')
                        price = float(prices[prices['trade_date'] == i]['open'])
                        shares_held = self.need_to_trade[stock][0] / price

                        if stop_loss:
                            if shares_held > 0:
                                self.book[stock] = [shares_held, self.need_to_trade[stock][2],
                                                    self.need_to_trade[stock][3], price * 0.9]
                            else:
                                self.book[stock] = [shares_held, self.need_to_trade[stock][2],
                                                    self.need_to_trade[stock][3], price * 1.1]
                        else:
                            self.book[stock] = [shares_held, self.need_to_trade[stock][2], self.need_to_trade[stock][3]]

                        if shares_held > 0:
                            self.long_notionals += self.need_to_trade[stock][0]
                        else:
                            self.short_notionals += self.need_to_trade[stock][0]

                        self.cash_position -= self.need_to_trade[stock][0]
                        self.notionals += self.need_to_trade[stock][0]
                        fee += self.transaction_cost * abs(self.need_to_trade[stock][0])
                        del self.need_to_trade[stock]

                if beta_hedge:
                    previous_hedge = self.hedge_notional
                    self.hedge_notional = -self.notionals * self.book_beta(date=i, current_index=j)
                    etf_prices = pd.read_csv(self.price_data_path + "510050.OF.csv")
                    etf_price = float(etf_prices[etf_prices['trade_date'] == i]['open'])
                    self.hedge_position = self.hedge_notional / etf_price
                    self.cash_position -= (self.hedge_notional - previous_hedge)

                if verbose:
                    print(i)
                    print("today's book")
                    print(self.book)
                    if beta_hedge:
                        print("total (dollar notional) beta of today's book = " + str(self.notionals *
                                                                    self.book_beta(date=i, current_index=j)))
                        print("hedging " + str(self.hedge_position) + " shares of SH50 ETF to neutralize beta")
                        print("beta after hedging = " + str(self.hedge_notional +
                                                            self.notionals * self.book_beta(date=i, current_index=j)))
                    print("need to trade")
                    print(self.need_to_trade)
                    print("")

            # if it is exit date, clear the positions
            if i in exit_dates:

                for stock in list(self.book):
                    if self.book[stock][1] == i:
                        prices = pd.read_csv(self.price_data_path + stock + '.csv')
                        price = float(prices[prices['trade_date'] == i]['open'])

                        self.cash_position += self.book[stock][0] * price
                        self.notionals -= self.book[stock][0] * price

                        if self.book[stock][0] > 0:
                            self.long_notionals -= self.book[stock][0] * price
                        else:
                            self.short_notionals -= self.book[stock][0] * price
                        fee += self.transaction_cost * abs(self.book[stock][0]) * price
                        del self.book[stock]

                if len(self.book) == 0 and beta_hedge:
                    self.cash_position += self.hedge_notional
                    fee += abs(self.hedge_notional) * self.transaction_cost
                    self.hedge_notional = 0
                    self.hedge_position = 0

                if verbose:
                    print(i)
                    print("today's book")
                    print(self.book)
                    print("need to trade")
                    print(self.need_to_trade)
                    print("")

            else:
                if store_in_bank:
                    if len(self.book) == 0:
                        self.cash_position *= (1 + self.bank_rate) ** (1 / 365)

                stop_loss_triggered = False

                # Check if any stop loss is triggered
                if stop_loss:
                    previous_hedge = self.hedge_notional
                    for stock in list(self.book):
                        prices = pd.read_csv(self.price_data_path + stock + '.csv')
                        price = prices[prices['trade_date'] == i]['open']

                        # if no price data found for a certain day, roll back until the closest day that we can find a price
                        k = 1
                        while len(price) == 0:
                            price = prices[prices['trade_date'] == self.account.index[j - k]]['open']
                            k += 1
                        price = float(price)

                        if price < self.book[stock][3] and self.book[stock][0] > 0:
                            print("stop_loss triggered for " + stock + ", liquidating " +
                                  str(self.book[stock][0]) + " of position")
                            print("stop loss price is " + str(self.book[stock][3]))
                            print("current price is " + str(price))

                            self.cash_position += self.book[stock][0] * price
                            self.notionals -= self.book[stock][0] * price
                            self.long_notionals -= self.book[stock][0] * price
                            fee += self.transaction_cost * abs(self.book[stock][0]) * price

                            del self.book[stock]
                            stop_loss_triggered = True

                        elif price > self.book[stock][3] and self.book[stock][0] < 0:
                            print("stop_loss triggered for " + stock + ", liquidating " +
                                  str(self.book[stock][0]) + " of position")
                            print("stop loss price is " + str(self.book[stock][3]))
                            print("current price is " + str(price))

                            self.cash_position += self.book[stock][0] * price
                            self.notionals -= self.book[stock][0] * price
                            self.short_notionals -= self.book[stock][0] * price
                            fee += self.transaction_cost * abs(self.book[stock][0]) * price

                            del self.book[stock]
                            stop_loss_triggered = True

                    if stop_loss_triggered:
                        if beta_hedge:
                            if len(self.book) != 0:
                                self.hedge_notional = -self.notionals * self.book_beta(date=i, current_index=j)
                                etf_prices = pd.read_csv(self.price_data_path + "510050.OF.csv")
                                etf_price = float(etf_prices[etf_prices['trade_date'] == i]['open'])
                                self.hedge_position = self.hedge_notional / etf_price
                                self.cash_position -= (self.hedge_notional - previous_hedge)
                                print("total (dollar notional) beta of today's book = " + str(self.notionals *
                                                                            self.book_beta(date=i, current_index=j)))
                                print("hedging " + str(self.hedge_position) + " shares of SH50 ETF to neutralize beta")
                                print(
                                    "beta after hedging = " + str(
                                        self.hedge_notional + self.notionals * self.book_beta(date=i, current_index=j)))
                            else:
                                self.cash_position += self.hedge_notional
                                fee += abs(self.hedge_notional) * self.transaction_cost
                                self.hedge_notional = 0
                                self.hedge_position = 0

                        print(i)
                        print(self.book)
                        print("")

            self.cash_position -= fee
            self.nav = self.cash_position + self.notionals + self.hedge_notional
            self.account.loc[i]['hedge_notional'] = self.hedge_notional
            self.account.loc[i]['hedge_position'] = self.hedge_position
            self.account.loc[i]['cash'] = self.cash_position
            self.account.loc[i]['fee_incurred'] = fee
            self.account.loc[i]['long_notionals'] = self.long_notionals
            self.account.loc[i]['short_notionals'] = self.short_notionals
            self.account.loc[i]['notionals'] = self.notionals
            self.account.loc[i]['NAV'] = self.nav
