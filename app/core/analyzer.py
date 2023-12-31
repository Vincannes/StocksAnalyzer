#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
from pprint import pprint

import pandas as pd

from app.core import constants as cst
from app.core.data_fetcher import DataFetcher


class Analyzer(object):
    fetcher = DataFetcher

    WEIGHT = {
        'bna': 2,
        'per': 3,
        'bvps': 2,
        'capit': 2,
        'ebitda': 2,
        'revenues': 1,
        'leverage': 1,
        'dividends': 1,
        'payout_ratio': 1,
        'profitability': 1,
    }

    def __init__(self, stock):
        self._fetcher = self.fetcher(stock)
        self._stock_name = stock

    @property
    def info(self):
        return self._fetcher

    @property
    def bna(self):
        return self._bna_history()

    @property
    def bvps(self):
        return self._bvps()

    @property
    def per(self):
        return self._per()

    @property
    def capitalisation(self):
        return self._capitalisation()

    @property
    def ebitda(self):
        return self._ebitda_history()

    @property
    def ebitda_marge(self):
        return self._ebitda_marge()

    @property
    def leverage(self):
        return self._leverage()

    @property
    def profitability(self):
        return self._profitability()

    @property
    def revenues(self):
        return self._revenue_history()

    @property
    def dividends(self):
        return self._dividends_history()

    @property
    def payout_ratio(self):
        return self._payout_ratio()

    # Analyze

    def bna_analyze(self):
        bna = self.bna
        value = "BNA "
        if bna == 0:
            value += "en décroissance."
        elif bna == 1:
            value += "crois depuis l'année précédente."
        elif bna == 2:
            value += "en constante croissance."
        return value

    def bvps_analyze(self):
        bvps = self.bvps
        value = "BVPS, prix réel de {}".format(self._fetcher.get_book_value_share())
        if bvps == 0:
            value += " sur-évaluee "
        elif bvps == 1:
            value += " sous-évaluee "
        value += "par rapport au cour de l action {}.".format(self._fetcher.get_price())
        return value

    def ebitda_analyze(self):
        ebida = self.ebitda
        value = "Le Bénéfice Avant Intérêts, Impôts, Dépréciation et Amortissement "
        if ebida == 0:
            value += " est en baisse."
        elif ebida == 1:
            value += " crois depuis l'année précédente."
        elif ebida == 2:
            value += " en constante croissance."
        return value

    def ebitda_marge_analyze(self):
        ebitda = self._ebitda_marge()
        print(ebitda)
        value = "EBITDA marge par rapport au Chiffre d'affaire"
        if ebitda == 0:
            value += " n'est pas bon"
        elif ebitda == 1:
            value += " est bonne"
        return value

    def per_analyze(self):
        per = self.per
        value = "PER {} ".format(self._fetcher.get_per())
        if per == 0:
            value += "sous-coté."
        elif per == 1:
            value += "normal."
        elif per == 2:
            value += "sur-coté."
        return value

    def capitalisation_analyze(self):
        capt = self.capitalisation
        value = "La capitalisation boursière est "
        if capt == 0:
            value += "est inférieur à 10 millions."
        elif capt == 1:
            value += "est inférieur à 100 millions."
        elif capt == 2:
            value += "entre 100 millions et 1 milliard."
        elif capt == 3:
            value += "superieur au milliard."
        return value

    def leverage_analyze(self):
        lev = self.leverage
        value = "Dette"
        if lev == 0:
            value += " sur-endette."
        if lev == 1:
            value += " pas trop eleve."
        if lev == 2:
            value += " parfaite."
        return value

    def profitability_analyze(self):
        prof = self.profitability
        value = "Rentabilite {}".format(self._fetcher.get_profitability())
        if prof == 0:
            value += " pas rentable"
        if prof == 1:
            value += " rentable"
        return value

    def revenues_analyze(self):
        revenue = self.revenues
        value = "Chiffre d'affaire"
        if revenue == 0:
            value += " en baisse."
        if revenue == 1:
            value += " crois depuis l'année précédente."
        if revenue == 2:
            value += " en constante croissance."
        return value

    def dividends_analyze(self):
        dividends = self.dividends
        value = "Les dividendes"
        if dividends == 0:
            value += " sont en baisse."
        elif dividends == 1:
            value += " crois depuis l'année précédente."
        elif dividends == 2:
            value += " en constante croissance."
        return value

    def payout_ratio_analyze(self):
        payout = self.payout_ratio
        value = "Taux de Distribution {}%".format(self._fetcher.get_payout_ratio())
        if payout == 0:
            value += " trop élevé."
        if payout == 1:
            value += " correct."
        return value

    def calculat_level(self):
        bna = self.bna * self.WEIGHT.get("bna")
        per = self.per * self.WEIGHT.get("per")
        bvps = self.bvps * self.WEIGHT.get("bvps")
        capit = self.capitalisation * self.WEIGHT.get("capit")
        revenues = self.revenues * self.WEIGHT.get("revenues")
        dividends = self.dividends * self.WEIGHT.get("dividends")
        payout_ratio = self.payout_ratio * self.WEIGHT.get("payout_ratio")

        profitability = self.profitability * self.WEIGHT.get("profitability")
        leverage = self.leverage * self.WEIGHT.get("leverage")
        ebitda = self.ebitda * self.WEIGHT.get("ebitda")

        score = bna + per + bvps + capit + revenues + dividends + payout_ratio + profitability + leverage + ebitda
        return score

    def show(self):
        msg = [
            self.bna_analyze(),
            self.bvps_analyze(),
            self.per_analyze(),
            self.capitalisation_analyze(),
            self.revenues_analyze(),
            self.dividends_analyze(),
            self.leverage_analyze(),
            self.payout_ratio_analyze(),
            self.ebitda_analyze(),
            self.ebitda_marge_analyze(),
            self.profitability_analyze(),
        ]
        return msg

    # PRIVATES

    def _bvps(self):
        """ prix reel de l entreprise
           marge de sécurité 0.7 * BVPS
        :return:
        """
        bvps = self._fetcher.get_book_value_share() * 0.7
        if float(bvps) > float(self._fetcher.get_price()):
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

    def _ebitda_marge(self):
        ebitda = self._fetcher.get_ebitda_marge()
        value = 0
        if ebitda < 30:
            value = 1
        return value

    def _ebitda_history(self):
        ebitda = self._fetcher.get_dividend_history()
        value = 0
        if ebitda.iloc[-1] > ebitda.iloc[-2]:
            value = 1
        if all(ebitda.iloc[i] > ebitda.iloc[i - 1] for i in range(1, len(ebitda))):
            value = 2
        return value

    def _leverage(self):
        lev = self._fetcher.get_leverage()
        value = 0
        if 1.5 < lev < 2:
            return 1
        elif lev < 1.5:
            return 2
        return value

    def _per(self):
        per = self._fetcher.get_per()
        value = 0
        if 10 < per < 22:
            value = 1
        elif per > 22:
            value = 2
        return value

    def _profitability(self):
        prof = self._fetcher.get_profitability()
        value = 0
        if prof < 10:
            value = 1
        return value

    def _revenue_history(self):
        revenues = self._fetcher.get_revenue_history()
        dates = [pd.to_datetime(date) for date in revenues.keys()]
        value = 0
        if revenues[dates[0]] > revenues[dates[1]]:
            value = 1
        if all(revenues[dates[i]] <= revenues[dates[i - 1]] for i in range(1, len(dates))):
            value = 2
        return value

    def _dividends_history(self):
        dividends = self._fetcher.get_dividend_history()
        value = 0
        if dividends.iloc[-1] > dividends.iloc[-2]:
            value = 1
        if all(dividends.iloc[i] > dividends.iloc[i - 1] for i in range(1, len(dividends))):
            value = 2
        return value

    def _bna_history(self):
        bna = self._fetcher.get_dividend_history()
        value = 0
        if bna.iloc[-1] > bna.iloc[-2]:
            value = 1
        if all(bna.iloc[i] > bna.iloc[i - 1] for i in range(1, len(bna))):
            value = 2
        return value

    def _payout_ratio(self):
        payout = self._fetcher.get_payout_ratio()
        value = 0
        if payout < 70:
            value = 1
        return value


if __name__ == "__main__":
    # analyze = Analyzer("MSFT")
    # print("per  ", analyze.per)
    # print("bvps ", analyze.bvps)
    # print("capit", analyze.capitalisation)
    # print("chiffre affaire", analyze.revenues)
    # print("dividendes", analyze.dividends)
    # print("bna", analyze.bna)
    # print("payout_ratio", analyze.payout_ratio)
    # pprint(analyze.show())

    actions = [
        "AI.PA",
        "AIR.PA",
        "ALO.PA",
        "CS.PA",
        "LR.PA",
    ]

    for stck in actions:
        analyze = Analyzer(stck)
        print(analyze.info.name)
        pprint(analyze.show())
        print(analyze.calculat_level())
        print("")
        # break