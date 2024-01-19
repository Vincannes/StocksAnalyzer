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
        return self._financer.data.get(cst.COMPAGNY_NAME, 0)

    @property
    def symbol(self):
        return self._financer.data.get(cst.SYMBOL, 0)

    @property
    def industry(self):
        return self._financer.data.get(cst.INDUSTRY, 0)

    @property
    def category(self):
        return self._financer.data.get("")

    def get_price(self):
        """Last Price
        :return:
        """
        return self._financer.data.get(cst.LAST_PRICE, 0)

    def get_assets_total(self):
        return self._financer.data.get(cst.ASSETS, 0)

    def get_bpa(self):
        """Ratio Benefice par Action (EPS)
        correspond au bénéfice dégagé par une société divisé par le nombre de titres formant le capital.
        :return:
        """
        return self._financer.data.get(cst.BPA, 0)

    def get_bpa_history(self):
        return self._financer.histories.get(cst.BPA_HST)

    def get_book_value(self):
        """ Valeur comptable, capitaux propres d'une entreprise .
        Elle correspond à la différence entre l'actif et le passif.
        :return:
        """
        return self._financer.data.get(cst.BOOK_VALUE, 0) * self.get_shares()

    def get_book_value_share(self):
        """ (Actif-Passif) / Nbr Parts
        :return:
        """
        return self._financer.data.get(cst.BOOK_VALUE, 0)

    def get_cash_flow(self):
        """Free Cash Flow
        cash disponible après investissements et dépenses
        :return:
        """
        return self._financer.data.get(cst.CASHFLOW, 0)

    def get_cash_flow_action(self):
        """Free Cash Flow Par action
        cash disponible après investissements et dépenses par action
        :return:
        """
        return self._financer.data.get(cst.CASHFLOW_ACTION, 0)

    def get_capitalisation(self):
        return self._financer.data.get(cst.CAPITALISATION, 0)

    def get_debt(self):
        return self._financer.data.get(cst.DEBT, 0)

    def get_dividend(self):
        return self._financer.data.get(cst.DIVIDENDE, 0)

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
         calculé par le cours divisé par le BNPA, permet de trier les entreprises en fonction de leur cherté.
         Plus le PER est élevé, plus une action est chère en Bourse, plus il est faible, moins elle est chère.
         Cherté d'une action
        :return:
        """
        price = self.get_price()
        bpa = self.get_bpa()
        if any([i == 0 for i in [price, bpa]]):
            return 0
        return round(price / bpa, 2)

    def get_payout_ratio(self):
        """Ratio distribution dividend par action
        orrespond à la rémunération qui est offerte par le dividende versé par une entreprise. Le rendement se calcule
        en rapportant le dividende au cours de Bourse par ction. Plus le rendement est élevé, plus la rémunération est forte.
        :return:
        """
        dividend = self.get_dividend()
        bpa = self.get_bpa()
        if any([i == 0 for i in [dividend, bpa]]):
            return 0
        return round((dividend / bpa) * 100, 2)

    def get_ebitda(self):
        """EBITDA
        Benefice Avant Internists Imposts & Advertisements
        :return:
        """
        return self._financer.data.get(cst.EBITDA, 0)

    def get_ebitda_marge(self):
        ebitda = self.get_ebitda()
        revenue = self.get_revenue()
        if any([i == 0 for i in [ebitda, revenue]]):
            return 0
        return (ebitda / revenue) * 100

    def get_ebitda_history(self):
        return self._financer.histories.get(cst.EBITDA_HST, [])

    def get_leverage(self):
        """ Si pas de Dette => regarder la trésorie
            EBITDA / DEBT
        :return:
        """
        ebitda = self.get_ebitda()
        debt = self.get_debt()
        if any([i == 0 for i in [ebitda, debt]]):
            return 0
        return round(ebitda / debt, 2)

    def get_ratio(self):
        """Coefficiant de liquidité
        capacite d une entreprise à couvrir ses obligations
        a court terme avec ses actifs a court terme
        :return:
        """
        return self._financer.data.get(cst.CURR_RATIO, 0)

    def get_price_history(self):
        return self._financer.histories.get(cst.CLOSE_HST)

    def get_profitability(self):
        """ Cours / (CashFlow / action)
        :return:
        """
        cash_flow = self.get_cash_flow()
        shares = self.get_shares()
        if any([i == 0 for i in [cash_flow, shares]]):
            return 0
        cashflow_action = abs(cash_flow / shares)
        return round(self.get_price() / cashflow_action, 2)

    def get_net_income(self):
        """ Resulat net
        :return:
        """
        return self._financer.data.get(cst.NET_INCOME, 0)

    def get_net_income_history(self):
        """ Resulat net
        :return:
        """
        return self._financer.histories.get(cst.NET_INCOME_HST, [])

    def get_revenue(self):
        """ Chiffre affaire
        :return:
        """
        return self._financer.data.get(cst.REVENUE, 0)

    def get_revenue_history(self):
        return self._financer.histories.get(cst.REVENUE_HST)

    def get_revenue_per_share(self):
        return self._financer.data.get(cst.REVENUE_SHARE, 0)

    def get_roa(self):
        """ Return On Asset
        Rapport resultat net / total actif
        :return: %
        """
        return  self._financer.data.get(cst.ROA, 0) * 100

    def get_roe(self):
        """ Return On Equity
        Rapport resultat net / capitaux propre
        :return: %
        """
        return self._financer.data.get(cst.ROE, 0) * 100

    def get_shares(self):
        """Number of shares
        :return:
        """
        return self._financer.data.get(cst.SHARES, 0)

    # calcul


if __name__ == '__main__':
    # stck = DataFetcher("GLE.PA")
    stck = DataFetcher("MSFT")
    # pprint(stck._financer.data)
    # pprint(stck._financer.histories)
    # quit()
    # print(stck._financer.get_dividends())
    # print([i for i, a in stck._financer.balance_sheet.items()])
    # print(stck._financer.info.get("totalCashPerShare"))
    # print(stck._financer.info.get("netIncomeToCommon"))
    # print(stck._financer.info.get("totalDebt"))
    # print(stck._financer.info.get("currentRatio"))
    # print(stck._financer.info.get("returnOnEquity"))
    # print(stck._financer.info.get("revenuePerShare"))
    # print("")
    # print(stck.get_price_history())
    print(stck.get_book_value())
    print(stck.get_book_value_share())
    quit()
    print("bpa", stck.get_bpa())
    print("per", stck.get_per())
    # print("shares", stck.get_shares())
    # print("ebit", stck.get_ebitda())
    # pprint(stck.get_ebitda_history())
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
    print("resultat net", stck.get_net_income())
    print("assets", stck.get_assets_total())
    print("resultat net history ", stck.get_net_income_history())
    print("price history ", stck.get_price_history())
    # print("revenue history", stck.get_revenue_history())
    # print("ROE", stck.get_bpa_history())
    # print("")
    # pprint(stck.name)
    # print("dividend history", stck.get_dividend_history())
    # print("bpa history", stck.get_bpa_history())
