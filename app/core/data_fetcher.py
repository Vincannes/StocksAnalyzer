#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
from pprint import pprint

import pandas as pd

from app.core import constants as cst
from app.adapters.finance_adapter import FinanceAdapters


class DataFetcher(object):
    fin_adapter = FinanceAdapters

    def __init__(self, stock):
        self._financer = self.fin_adapter(stock)
        self._stock_name = stock

    @property
    def name(self):
        return self._financer.data.get(cst.COMPAGNY_NAME)

    @property
    def symbol(self):
        return self._financer.data.get(cst.SYMBOL)

    @property
    def industry(self):
        return self._financer.data.get(cst.INDUSTRY)

    def get_price(self):
        """Last Price
        :return:
        """
        return self._financer.data.get(cst.LAST_PRICE)

    def get_assets_total(self):
        return self._financer.data.get(cst.ASSETS)

    def get_bpa(self):
        """Ratio Benefice par Action (EPS)
        :return:
        """
        return self._financer.data.get(cst.BPA)

    def get_bpa_history(self):
        return self._financer.histories.get(cst.BPA_HST)

    def get_book_value(self):
        return self._financer.data.get(cst.BOOK_VALUE) * self.get_shares()

    def get_book_value_share(self):
        """ (Actif-Passif) / Nbr Parts
        :return:
        """
        return self._financer.data.get(cst.BOOK_VALUE)

    def get_cash_flow(self):
        return self._financer.data.get(cst.CASHFLOW)

    def get_cash_flow_action(self):
        return self._financer.data.get(cst.CASHFLOW_ACTION)

    def get_capitalisation(self):
        return self._financer.data.get(cst.CAPITALISATION)

    def get_debt(self):
        return self._financer.data[cst.DEBT]

    def get_dividend(self):
        return self._financer.data.get(cst.DIVIDENDE)

    def get_dividend_history(self):
        dividends = self._financer.dividends
        df = pd.DataFrame(dividends)
        df.index = pd.to_datetime(df.index)
        df['Year'] = df.index.year
        df_last_five_years = df[df['Year'] >= df['Year'].max() - 4]
        average_dividends_by_year = df_last_five_years.groupby('Year')['Dividends'].sum()
        return average_dividends_by_year

    def get_per(self):
        """Price Earning Ratio
        :return:
        """
        return round(self.get_price() / self.get_bpa(), 2)

    def get_payout_ratio(self):
        """Ratio distribution dividend par action
        :return:
        """
        return round((self.get_dividend() / self.get_bpa()) * 100, 2)

    def get_ebitda(self):
        """EBITDA
        Benefice Avant Internists Imposts & Advertisements
        :return:
        """
        return self._financer.data.get(cst.EBITDA, 0)

    def get_ebitda_marge(self):
        return (self.get_ebitda() / self.get_revenue()) * 100

    def get_ebitda_history(self):
        return self._financer.histories.get(cst.EBITDA_HST)

    def get_leverage(self):
        """ Si pas de Dette => regarder la trésorie
            EBITDA / DEBT
        :return:
        """
        return round(self.get_ebitda() / self.get_debt(), 2)

    def get_ratio(self):
        """Coefficiant de liquidité
        capacite d une entreprise à couvrir ses obligations
        a court terme avec ses actifs a court terme
        :return:
        """
        return self._financer.data.get(cst.CURR_RATIO)

    def get_profitability(self):
        """ Cours / (CashFlow / action)
        :return:
        """
        cashflow_action = abs(self.get_cash_flow() / self.get_shares())
        return round(self.get_price() / cashflow_action, 2)

    def get_net_income(self):
        """ Resulat net
        :return:
        """
        return self._financer.data.get(cst.NET_INCOME)

    def get_revenue(self):
        """ Chiffre affaire
        :return:
        """
        return self._financer.data.get(cst.REVENUE)

    def get_revenue_history(self):
        return self._financer.histories.get(cst.REVENUE_HST)

    def get_revenue_per_share(self):
        return self._financer.data.get(cst.REVENUE_SHARE)

    def get_roa(self):
        """ Return On Asset
        Rapport resultat net / total actif
        :return: %
        """
        return  self._financer.data.get(cst.ROA) * 100

    def get_roe(self):
        """ Return On Equity
        Rapport resultat net / capitaux propre
        :return: %
        """
        return self._financer.data.get(cst.ROE) * 100

    def get_shares(self):
        """Number of shares
        :return:
        """
        return self._financer.data.get(cst.SHARES)

    # calcul


if __name__ == '__main__':
    stck = DataFetcher("MSFT")
    # pprint(stck._financer.data)
    # pprint(stck._financer.histories)
    # print(stck._financer.get_dividends())
    # print([i for i, a in stck._financer.balance_sheet.items()])
    # print(stck._financer.info.get("totalCashPerShare"))
    # print(stck._financer.info.get("netIncomeToCommon"))
    # print(stck._financer.info.get("totalDebt"))
    # print(stck._financer.info.get("currentRatio"))
    # print(stck._financer.info.get("returnOnEquity"))
    # print(stck._financer.info.get("revenuePerShare"))
    # print("")
    print("bpa", stck.get_bpa())
    print("per", stck.get_per())
    print("shares", stck.get_shares())
    print("ebit", stck.get_ebitda())
    pprint(stck.get_ebitda_history())
    print("revenue", stck.get_revenue())
    print("revenue share", stck.get_revenue_per_share())
    print("cash flow", stck.get_cash_flow())
    print("dividende", stck.get_dividend())
    print("debt", stck.get_debt())
    print("leverage", stck.get_leverage())
    print("ratio", stck.get_ratio())
    print("book value", stck.get_book_value())
    print("book value share", stck.get_book_value_share())
    print("capitalisation", stck.get_capitalisation())
    print("payout", stck.get_payout_ratio())
    print("")
    print("revenue history", stck.get_revenue_history())
    print("")
    print("rn", stck.get_net_income())
    print("assets", stck.get_assets_total())
    print("ROE", stck.get_bpa_history())
    print("")
    pprint(stck.name)
    print("dividend history", stck.get_dividend_history())
    print("bpa history", stck.get_bpa_history())
