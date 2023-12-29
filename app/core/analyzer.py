#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

from app.core import constants as cst
from app.core.data_fetcher import DataFetcher


class Analyzer(object):
    fetcher = DataFetcher

    def __init__(self, stock):
        self._fetcher = self.fetcher(stock)
        self._stock_name = stock

    @property
    def bvps(self):
        return self._bvps()

    @property
    def per(self):
        return self._per()

    @property
    def capitalisation(self):
        return self._capitalisation()

    # PRIVATES

    def _bvps(self):
        bvps = self._fetcher.get_book_value_share() * 0.7
        if float(bvps) < float(self._fetcher.get_price()):
            value = 0
        else:
            value = 1
        return value

    def _capitalisation(self):
        capit = self._fetcher.get_capitalisation()
        value = 3
        if capit < 10000000:
            value = 0
        if capit < 100000000:
            value = 1
        if capit < 1000000000:
            value = 2
        return value

    def _per(self):
        per = self._fetcher.get_per()
        value = 0
        if 10 < per < 22:
            value = 1
        elif per > 22:
            value = 2
        return value


if __name__ == "__main__":
    analyze = Analyzer("MSFT")
    print("per  ", analyze.per)
    print("bvps ", analyze.bvps)
    print("capit", analyze.capitalisation)
