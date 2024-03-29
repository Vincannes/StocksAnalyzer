#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import datetime
import yfinance as yf
from pprint import pprint

from app.core import constants as cst
from app.core.utils import DataToDict


class FinanceAdapters(object):

    def __init__(self, stock):
        self._stock_name = stock
        self._stock = yf.Ticker(stock)
        self._data = {}
        self._histories = {}
        self._load_datas()

    @property
    def data(self):
        return self._data

    @property
    def histories(self):
        return self._histories

    @property
    def dividends(self):
        return self._get_dividends()

    # PRIVATES

    def _load_datas(self):
        for key, val in self._stock.info.items():
            self._data[key] = val
        self._data[cst.ASSETS] = DataToDict(self._stock.balance_sheet).get(cst.ASSETS)[0]
        self._histories = DataToDict(self._stock.get_financials())
        self._histories.append(self._get_price_hst())
        self._histories.append(self._balance_sheet())
        self._histories.append(self._cashflow())

    def _balance_sheet(self):
        return self._stock.balance_sheet

    def _financials(self):
        return self._stock.get_financials()

    def _get_actions(self):
        return self._stock.actions

    def get_earnings(self):
        return self._stock.earnings

    def _cashflow(self):
        return self._stock.cashflow

    def _get_dividends(self):
        return self._stock.dividends

    def _get_splits(self):
        return self._stock.splits

    def _get_capital(self):
        return self._stock.capital_gains

    def _get_price_hst(self):
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=365 * 5)

        price = yf.download(self._stock_name, interval="3mo", start=start_date, end=end_date)[cst.CLOSE_HST]
        return price.resample('Y').mean()

    def _get_resultat_compte(self):
        """
        EBITDA / EBIT / EPS /Tax Provision / Gross Profit
        Basic Average Shares / Total Revenue
        :return:
        """
        return self._stock.income_stmt

    def _get_balance_sheet(self):
        """
        Total Cash / Total Cash per Share /
        Total Debt / Net Debt
        :return:
        """
        return self._stock.balance_sheet

    def _get_cash_flow(self):
        return self._stock.cashflow


if __name__ == '__main__':
    from pprint import pprint
    stck = FinanceAdapters("MSFT")
    # pprint(stck.data)
    pprint(stck.histories)
    # print(stck._get_price_hst())
    # pprint(stck._get_dividends())
    # print(stck.financials)
    # print(stck.financials.get("TotalRevenue"))
