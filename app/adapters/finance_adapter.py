#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import yfinance as yf


class FinanceAdapters(object):

    def __init__(self, stock):
        self._stock_name = stock
        self._stock = yf.Ticker(stock)

    def get_price(self):
        a = self._stock.info
        return a#.get("currentPrice")

    def get_actions(self):
        return self._stock.actions

    def get_dividends(self):
        return self._stock.dividends

    def get_splits(self):
        return self._stock.splits

    def get_capital(self):
        return self._stock.capital_gains

    def get_resultat_compte(self):
        """
        EBITDA / EBIT / EPS /Tax Provision / Gross Profit
        Basic Average Shares / Total Revenue
        :return:
        """
        return self._stock.income_stmt

    def get_balance_sheet(self):
        """
        Total Cash / Total Cash per Share /
        Total Debt / Net Debt
        :return:
        """
        return self._stock.balance_sheet

    def get_cash_flow(self):
        return self._stock.cashflow


if __name__ == '__main__':
    stck = FinanceAdapters("MSFT")
    print(type(stck.get_price()))

