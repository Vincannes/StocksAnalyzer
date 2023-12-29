#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

from app.core import constants as cst
from app.adapters.finance_adapter import FinanceAdapters


class DataFetcher(object):
    fin_adapter = FinanceAdapters

    def __init__(self, stock):
        self._financer = self.fin_adapter(stock)
        self._stock_name = stock

    def get_price(self):
        """Last Price
        :return:
        """
        return self._financer.get_price()

    def get_bpa(self):
        """Ratio Benefice par Action
        :return:
        """
        return self._financer.info[cst.BPA]

    def get_book_value(self):
        return self._financer.info.get(cst.BOOK_VALUE) * self.get_shares()

    def get_book_value_share(self):
        return self._financer.info.get(cst.BOOK_VALUE)

    def get_cash_flow(self):
        return self._financer.info[cst.CASHFLOW]

    def get_cash_flow_action(self):
        return self._financer.info[cst.CASHFLOW_ACTION]

    def get_capitalisation(self):
        return self._financer.info.get(cst.CAPITALISATION)

    def get_debt(self):
        return self._financer.info[cst.DEBT]

    def get_dividend(self):
        return self._financer.info[cst.DIVIDENDE]

    def get_per(self):
        """Price Earning Ratio
        :return:
        """
        return self.get_price() / self.get_bpa()

    def get_ebitda(self):
        """EBITDA
        Benefice Avant Internists Imposts & Advertisements
        :return:
        """
        return self._financer.info.get(cst.EBITDA, 0)

    def get_ratio(self):
        """Coefficiant de liquidité
        capacite d une entreprise à couvrir ses obligations
        a court terme avec ses actifs a court terme
        :return:
        """
        return self._financer.info.get(cst.CURR_RATIO)

    def get_revenue(self):
        """ Chiffre affaire
        :return:
        """
        return self._financer.info.get(cst.REVENUE)

    def get_revenue_per_share(self):
        return self._financer.info.get(cst.REVENUE_SHARE)

    def get_roa(self):
        return

    def get_roe(self):
        return

    def get_shares(self):
        """Number of shares
        :return:
        """
        return self._financer.info.get(cst.SHARES)

    # calcul


if __name__ == '__main__':
    stck = DataFetcher("MSFT")
    print(stck._financer.info.keys())
    # print(stck._financer.info.get("totalCashPerShare"))
    # print(stck._financer.info.get("totalDebt"))
    # print(stck._financer.info.get("currentRatio"))
    # print(stck._financer.info.get("revenuePerShare"))
    print("")
    print("bpa", stck.get_bpa())
    print("per", stck.get_per())
    print("shares", stck.get_shares())
    print("ebit", stck.get_ebitda())
    print("revenue", stck.get_revenue())
    print("revenue share", stck.get_revenue_per_share())
    print("cash flow", stck.get_cash_flow())
    print("dividende", stck.get_dividend())
    print("debt", stck.get_debt())
    print("ratio", stck.get_ratio())
    print("book value", stck.get_book_value())
    print("book value share", stck.get_book_value_share())
    print("capitalisation", stck.get_capitalisation())
