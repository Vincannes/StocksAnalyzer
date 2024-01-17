#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import yfinance as yf

from app.core.utils import DataToDict


class FinanceAdapters(object):

    def __init__(self, stock):
        self._stock_name = stock
        self._stock = yf.Ticker(stock)
        self._info = self._stock.info

    @property
    def info(self):
        return self._info

    @property
    def balance_sheet(self):
        return DataToDict(self._stock.balance_sheet)

    @property
    def financials(self):
        return DataToDict(self._stock.get_financials())

    def get_price(self):
        return self._info.get("currentPrice")

    def get_actions(self):
        return self._stock.actions

    def get_earnings(self):
        return self._stock.earnings

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
    print(stck.info)
    print(stck.financials)
    # print(stck.financials.get("TotalRevenue"))
