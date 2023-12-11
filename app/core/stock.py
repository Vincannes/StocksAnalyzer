#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

from app.adapters.finance_adapter import FinanceAdapters


class Stock(object):
    fin_adapter = FinanceAdapters

    def __init__(self, stock):
        self.financer = self.fin_adapter(stock)
        self._stock_name = stock

    def actions(self):
        pass

    @property
    def price(self):
        return

    @property
    def bna(self):
        return

    @property
    def bvps(self):
        return

    @property
    def capitalisaton(self):
        return

    @property
    def chiffre_affaire(self):
        return

    @property
    def dette(self):
        return

    @property
    def per(self):
        return

    @property
    def roa(self):
        return

    @property
    def roe(self):
        return

    @property
    def taux_distribution(self):
        return
