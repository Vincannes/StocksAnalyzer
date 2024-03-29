#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
from pprint import pprint

import numpy as np
import pandas as pd

from app.core import constants as cst
from app.core.data_fetcher import DataFetcher

def format_scientific(value):
    return '{:.2f}'.format(value)


class Analyzer(object):
    fetcher = DataFetcher

    WEIGHT = {
        'bna': 1,           # BNA (Bénéfice Net par Action)
        'per': 3,           # PER (Price to Earnings Ratio)
        'roa': 2,           # ROA (Return on Assets)
        'roe': 2,           # ROE (Return on Equity)
        'bvps': 2,          # BVPS (Book Value per Share)
        'capit': 2,         # Capitalisation
        'ebitda': 1,        # EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization)
        'cashflow': 1,      # Cash Flow
        'revenues': 2,      # Revenues (Chiffre d'affaires)
        'leverage': 1,      # Leverage (Dette)
        'dividends': 2,     # Dividends
        'payout_ratio': 2,  # Payout Ratio (Taux de Distribution)
        'profitability': 2, # Rentabilité
        'resultat_net': 3,  # Résultat Net
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
    def cashflow(self):
        return self._cash_flow()

    @property
    def cashflow_history(self):
        return self._cash_flow_history()

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
    def dividends_efficiancy(self):
        return self._dividend_efficiency()

    @property
    def price(self):
        return self._price_evolution()

    @property
    def payout_ratio(self):
        return self._payout_ratio()

    @property
    def roa(self):
        return self._roa()

    @property
    def roe(self):
        return self._roe()

    @property
    def resulat_net(self):
        return self._net_income_history()

    # Analyze

    def bna_analyze(self):
        """TODO
        :return:
        """
        bna = self.bna
        value = "BNA "
        # if bna == 0:
        #     value += "en décroissance."
        # elif bna == 1:
        #     value += "crois depuis l'année précédente."
        # elif bna == 2:
        #     value += "en constante croissance: "
        value += "{}".format(self._fetcher.get_bpa())
        return value

    def bvps_analyze(self):
        """Verifie si BVPS < 0.7 * cours actuel
        Doit acheter a 0.7 * Cours actuel
        :return:
        """
        bvps = self.bvps
        value = "BVPS : prix réel de {}€".format(self._fetcher.get_book_value_share())
        if bvps == 0:
            value += " sur-évaluee "
        elif bvps == 1:
            value += " sous-évaluee "
        value += "par rapport à sa valeur réel."
        return value

    def cashflow_analyze(self):
        """Est-ce que CashFlow est positif
        :return:
        """
        cash = self._cash_flow
        value = "Tresorie: "
        if cash == 0:
            value += "négatif: "
        elif cash == 1:
            value += "positif: "
        value += "{:,.0f}M €".format(int(self._fetcher.get_cash_flow())/10**6)
        value += " > 0$"
        return value

    def cashflow_history_analyze(self):
        """CashFlow est positif au cours des 5 dernieres annees.
        :return:
        """
        cash = self._cash_flow_history()
        value = "Tresorie "
        if cash == 0:
            value += "en baisse: "
        elif cash == 1:
            value += "globalement en baisse: "
        elif cash == 2:
            value += "sans croissance particuliere: "
        elif cash == 3:
            value += "globalement en hausse: "
        elif cash == 4:
            value += "en hausse: "
        value += " ".join(["{:,.0f}M €".format(int(i)/10**6) for i in self._fetcher.get_cash_flow_history()])
        return value

    def ebitda_analyze(self):
        """Verifie si l EBITDA augmente au cours des 5 derniees annees.
        :return:
        """
        ebida = self.ebitda
        value = "EBITDA: Le Benefice Avant Interets, Impots, Depreciation et Amortissement "
        if ebida == 0:
            value += " est en baisse."
        elif ebida == 1:
            value += " crois depuis l annee precedente."
        elif ebida == 2:
            value += " en constante croissance."
        value += " ".join(["{:,.0f}M".format(int(i)/10**6) for i in self._fetcher.get_ebitda_history() if i])
        return value

    def ebitda_marge_analyze(self):
        """ Verifie si l EBITDA est > 30%.
        A une activite plus rentable.
        :return:
        """
        ebitda = self._ebitda_marge()
        value = "EBITDA marge par rapport au Chiffre d affaire"
        if ebitda == 0:
            value += " n est pas bon:"
        elif ebitda == 1:
            value += " est bonne:"
        value += " {}%".format(round(self._fetcher.get_ebitda_marge(), 2))
        value += " > 30%"
        return value

    def per_analyze(self):
        """ 10 < PER < 22
        Le prix est trop eleve, surevalue
        :return:
        """
        per = self.per
        value = "PER {} ".format(self._fetcher.get_per())
        if per == 0:
            value += "sous-coté."
        elif per == 1:
            value += "normal."
        elif per == 2:
            value += "sur-coté."
        value += " < 22"
        return value

    def capitalisation_analyze(self):
        """ Verifie si superieur a 10 millions $ ou superieur a 100 millions $
        ou superieur a 1 milliard $
        :return:
        """
        capt = self.capitalisation
        value = "Capitalisation boursiere est "
        if capt == 0:
            value += "est inferieur a 10 millions"
        elif capt == 1:
            value += "est inferieur a 100 millions"
        elif capt == 2:
            value += "entre 100 millions et 1 milliard"
        elif capt == 3:
            value += "superieur a 1 milliard"
        value += ": {:,.0f}M €".format(int(self._fetcher.get_capitalisation())/10**6)
        return value

    def leverage_analyze(self):
        """% de dette doit etre le plus bas < 1.5
        :return:
        """
        lev = self.leverage
        value = "Dette"
        if lev == 0:
            value += " sur-endette: "
        if lev == 1:
            value += " pas trop eleve: "
        if lev == 2:
            value += " parfaite: "
        value += "{}%".format(self._fetcher.get_leverage())
        value += " < 1.5%"
        return value

    def profitability_analyze(self):
        """Quel attractif une action specifique est par rapport a d autres actions.
        Plus le C/CF est bas, plus l action est evaluee meilleur marche.
        Rentabilité < 7
        :return:
        """
        prof = self.profitability
        value = "Rentabilite"
        if prof == 0:
            value += " pas rentable:"
        if prof == 1:
            value += " rentable:"
        value += " {}%".format(self._fetcher.get_profitability())
        value += " < 7%."
        return value

    def resultat_net_analyze(self):
        """Verifie si le resultat net augmente au cours des 5 dernieres annees.
        :return:
        """
        net_income = self.resulat_net
        value = "Resulat net {}".format(self._fetcher.get_profitability())
        if net_income == 0:
            value += " strictement décroissant: "
        if net_income == 1:
            value += " globalement décroissant: "
        if net_income == 2:
            value += " neutre: "
        if net_income == 3:
            value += " globalement croissant: "
        if net_income == 4:
            value += " strictement croissant: "
        value += " ".join(["{}M€ ".format(int(i)/10**6) for i in self._fetcher.get_net_income_history()])
        return value

    def revenues_analyze(self):
        """Verifie si le chiffre d affaire augmente au cours des 5 dernieres annees.
        :return:
        """
        revenue = self.revenues
        value = "Chiffre d'affaire"
        if revenue == 0:
            value += " en baisse: "
        if revenue == 1:
            value += " crois depuis l'année précédente: "
        if revenue == 2:
            value += " en constante croissance: "
        value += " ".join(["{}M €".format(int(i)/10**6) for i in self._fetcher.get_revenue_history()])
        return value

    def dividends_analyze(self):
        """Verifie si les dividendes augmentent au cours des 5 dernieres annees.
        :return:
        """
        dividends = self.dividends
        value = "Les dividendes"
        if dividends == 0:
            value += " sont en baisse: "
        elif dividends == 1:
            value += " crois depuis l'année précédente: "
        elif dividends == 2:
            value += " en constante croissance: "
        value += " ".join(["{}€".format(round(i, 2)) for i in self._fetcher.get_dividend_history()])
        return value

    def dividends_efficiancy_analyze(self):
        """Verifie si le rendement par dividende n est pas trop eleve.
        En %.
        :return:
        """
        price = self.dividends_efficiancy
        value = "Rendement par dividende "
        if price == 4:
            value += "faible "
        if price == 3:
            value += "assez faible "
        if price == 2:
            value += "neutre "
        if price == 1:
            value += "assez fort "
        if price == 0:
            value += "fort "

        value += "avec un rendement de : {}%".format(round((self._fetcher.get_dividend()/self._fetcher.get_price())*100, 2))
        value += " < 3%"
        return value

    def payout_ratio_analyze(self):
        """Taux de Distribution. Si le reverse trop de dividendes > 70%.
        :return:
        """
        payout = self.payout_ratio
        value = "Taux de Distribution"
        if payout == 0:
            value += " trop élevé."
        if payout == 1:
            value += " correct."
        value += " {}%".format(self._fetcher.get_payout_ratio())
        value += " < 70%"
        return value

    def price_analyze(self):
        """Verifie si au cours des 5 dernieres annees, le prix de l action augmente.
        :return:
        """
        price = self.price
        value = "Evolution du prix "
        if price == 0:
            value += " strictement décroissant: "
        if price == 1:
            value += " globalement décroissant: "
        if price == 2:
            value += " neutre: "
        if price == 3:
            value += " globalement croissant: "
        if price == 4:
            value += " strictement croissant: "

        value += " ".join(
            ["{}€".format(round(i, 2)) for i in self._fetcher.get_price_history() if i != 0]
        )
        return value

    def roa_analyze(self):
        """Si le ROA est supérieur à 10%.
        La société génère assez de bénéfice avec ses actifs.
        :return:
        """
        roa = self.roa
        value = "ROA de"
        if roa == 0:
            value += " mauvaise rentabilite: "
        if roa == 1:
            value += " bonne rentabilite: "

        value += "{}%".format(round(self._fetcher.get_roa(), 2))
        value += " > 10%"
        return value

    def roe_analyze(self):
        """Si le ROE est supérieur à 10%.
        La société génère assez de bénéfice avec ses actifs.
        :return:
        """
        roe = self.roe
        value = "ROE a un"
        if roe == 0:
            value += " resultat mediocre: "
        if roe == 1:
            value += " resultat acceptable: "

        value += "{}%".format(round(self._fetcher.get_roe(), 2))
        value += " > 10%"
        return value

    def calculate_level(self):
        bna = self.bna * self.WEIGHT.get("bna")
        per = self.per * self.WEIGHT.get("per")
        bvps = self.bvps * self.WEIGHT.get("bvps")
        cash = self.cashflow * self.WEIGHT.get("cashflow")
        cash_hst = self.cashflow_history * self.WEIGHT.get("cashflow")
        capit = self.capitalisation * self.WEIGHT.get("capit")
        revenues = self.revenues * self.WEIGHT.get("revenues")
        dividends = self.dividends * self.WEIGHT.get("dividends")
        dividends_eff = self.dividends_efficiancy * self.WEIGHT.get("dividends")
        payout_ratio = self.payout_ratio * self.WEIGHT.get("payout_ratio")

        profitability = self.profitability * self.WEIGHT.get("profitability")
        leverage = self.leverage * self.WEIGHT.get("leverage")
        ebitda = self.ebitda * self.WEIGHT.get("ebitda")
        resulat_net = self.resulat_net * self.WEIGHT.get("resultat_net")

        roa = self.roa * self.WEIGHT.get("roa")
        roe = self.roe * self.WEIGHT.get("roe")

        score = bna + per + bvps + capit + revenues + dividends + payout_ratio + profitability + leverage + ebitda
        score += roa + roe + cash + resulat_net + dividends_eff + cash_hst
        return score

    def show(self):
        msg = [
            "Prix: {}€".format(self._fetcher.get_price()),
            self.bna_analyze(),
            self.bvps_analyze(),
            self.per_analyze(),
            self.capitalisation_analyze(),
            self.revenues_analyze(),
            self.cashflow_analyze(),
            self.cashflow_history_analyze(),
            self.dividends_analyze(),
            self.dividends_efficiancy_analyze(),
            self.resultat_net_analyze(),
            self.leverage_analyze(),
            self.payout_ratio_analyze(),
            self.ebitda_analyze(),
            self.ebitda_marge_analyze(),
            self.profitability_analyze(),
            self.roa_analyze(),
            self.roe_analyze(),
        ]
        return msg

    # PRIVATES

    def _bvps(self):
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

    def _cash_flow(self):
        value = 0
        cash = self._fetcher.get_cash_flow()
        if cash > 0:
            value = 1
        return value

    def _cash_flow_history(self):
        casf_flow_hst = self._fetcher.get_cash_flow_history()

        if len(casf_flow_hst) == 0:
            return 0

        series_data = []
        last_year = None
        for year, group in casf_flow_hst.groupby(casf_flow_hst.index.year):
            for i in group:
                if last_year != year:
                    last_year = year
                    series_data.append(i)

        first_year_index = next((index for index, value in enumerate(series_data) if value != 0.0), None)
        last_year_index = next(
            (len(series_data) - index - 1 for index, value in enumerate(series_data[::-1]) if value != 0.0), None
        )

        fully_increase = all(i < j for i, j in zip(series_data[first_year_index:last_year_index], series_data[2:]))
        fully_decrease = all(i > j for i, j in zip(series_data[first_year_index:last_year_index], series_data[2:]))
        if fully_decrease:
            value = 0
        elif fully_increase:
            value = 4
        elif series_data[first_year_index] > series_data[last_year_index]:
            value = 1
        elif series_data[first_year_index] < series_data[last_year_index]:
            value = 3
        else:
            value = 2

        return value

    def _ebitda_marge(self):
        ebitda = self._fetcher.get_ebitda_marge()
        value = 0
        if ebitda > 30:
            value = 1
        return value

    def _ebitda_history(self):
        ebitda = self._fetcher.get_ebitda_history()
        value = 0
        if len(ebitda) == 0:
            return value
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
        if len(revenues) == 0:
            return value
        if revenues[dates[0]] > revenues[dates[1]]:
            value = 1
        if all(revenues[dates[i]] <= revenues[dates[i - 1]] for i in range(1, len(dates))):
            value = 2
        return value

    def _net_income_history(self):
        net_incomes = self._fetcher.get_net_income_history()

        if len(net_incomes) == 0:
            return 0

        tendance_3 = net_incomes.diff(2).fillna(0).apply(np.sign).iloc[0]
        tendance_5 = net_incomes.diff(4).fillna(0).apply(np.sign).iloc[0]

        if tendance_3 == -1 and tendance_5 == -1:
            value = 0
        elif tendance_3 == -1 or tendance_5 == -1:
            value = 1
        elif tendance_3 == 0 or tendance_5 == 0:
            value = 2
        elif tendance_3 == 1 or tendance_5 == 1:
            value = 3
        else:
            value = 4
        return value

    def _dividends_history(self):
        dividends = self._fetcher.get_dividend_history()
        value = 0
        if len(dividends) == 0:
            return value
        if dividends.iloc[-1] > dividends.iloc[-2]:
            value = 1
        if all(dividends.iloc[i] > dividends.iloc[i - 1] for i in range(1, len(dividends))):
            value = 2
        return value

    def _dividend_efficiency(self):
        dividend = self._fetcher.get_dividend()
        price_shares = self._fetcher.get_price()
        rendement = (dividend / price_shares) * 100

        if rendement <= 0:
            value = 4
        elif 0 < rendement < 1:
            value = 3
        elif 1 < rendement < 2:
            value = 2
        elif 2 < rendement < 3:
            value = 1
        else:
            value = 0

        return value

    def _bna_history(self):
        bna = self._fetcher.get_bpa()
        value = 0
        # if bna.iloc[-1] > bna.iloc[-2]:
        #     value = 1
        # if all(bna.iloc[i] > bna.iloc[i - 1] for i in range(1, len(bna))):
        #     value = 2
        return value

    def _payout_ratio(self):
        payout = self._fetcher.get_payout_ratio()
        value = 0
        if payout < 70:
            value = 1
        return value

    def _price_evolution(self):
        prices = self._fetcher.get_price_history()

        if len(prices) == 0:
            return 0

        tendance_3 = prices.diff(2).fillna(0).apply(np.sign).iloc[0]
        tendance_5 = prices.diff(4).fillna(0).apply(np.sign).iloc[0]

        if tendance_3 == -1 and tendance_5 == -1:
            value = 0
        elif tendance_3 == -1 or tendance_5 == -1:
            value = 1
        elif tendance_3 == 0 or tendance_5 == 0:
            value = 2
        elif tendance_3 == 1 or tendance_5 == 1:
            value = 3
        else:
            value = 4

        return value

    def _roa(self):
        roa = self._fetcher.get_roa()
        value = 0
        if roa >= 10:
            value = 1
        return value

    def _roe(self):
        roe = self._fetcher.get_roe()
        value = 0
        if roe >= 10:
            value = 1
        return value



if __name__ == "__main__":
    # analyze = Analyzer("MSFT")
    # print("per  ", analyze.per)
    # print("bvps ", analyze.bvps)
    # print("bvps ", analyze.bvps)
    # print("dividend ", analyze.dividends_efficiancy_analyze())
    # print("cashflow_history ", analyze._net_income_history())
    # print("cashflow_history ", analyze.cashflow_history_analyze())
    # print("price ", analyze.price_analyze())
    # print("resultat net ", analyze.resultat_net_analyze())
    # print("capit", analyze.capitalisation)
    # print("chiffre affaire", analyze.revenues)
    # print("dividendes", analyze.dividends)
    # print("bna", analyze.bna)
    # print("payout_ratio", analyze.payout_ratio, analyze.payout_ratio_analyze())
    # pprint(analyze.show())
    # pprint(analyze.calculate_level())
    # quit()
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
        print(analyze.calculate_level())
        print("")
        # break
