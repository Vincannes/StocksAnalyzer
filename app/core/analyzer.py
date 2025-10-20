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


def history_data_to_string(data):
    return " ; ".join(["{} {}M €".format(year.strftime('%Y'), int(value) / 10 ** 6) for year, value in data.items()])


def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 0
    return (value - min_val) / (max_val - min_val)


class Analyzer(object):
    fetcher = DataFetcher

    MAX_SCORE = {
        'bna': 2,
        'per': 2,
        'roa': 3,
        'roe': 1,
        'bvps': 1,
        'ebitda': 2,
        'cashflow': 1,
        'revenues': 2,
        'leverage': 2,
        'dividends': 2,
        'payout_ratio': 1,
        'profitability': 1,
        'resultat_net': 4,
        'capitalisation': 3,
        'long_term_debt_history': 4,
    }

    WEIGHT = {
        'bna': {'range': (0, 10), 'weight': 2.0},  # Benefice net par action
        'per': {'range': (0, 30), 'weight': 1.5},  # Price/Earnings
        'roa': {'range': (0, 20), 'weight': 2.0},  # Return on Assets
        'roe': {'range': (0, 30), 'weight': 2.0},  # Return on Equity
        'bvps': {'range': (0, 50), 'weight': 1.0},  # Valeur comptable
        'ebitda': {'range': (0, 100), 'weight': 2.0},  # EBITDA
        'cashflow': {'range': (0, 100), 'weight': 2.0},  # Flux de tresorerie
        'revenues': {'range': (0, 1000), 'weight': 1.5},  # Chiffre d affaires
        'leverage': {'range': (0, 5), 'weight': 1.5},  # Dette
        'dividends': {'range': (0, 10), 'weight': 1.0},  # Dividendes
        'payout_ratio': {'range': (0, 100), 'weight': 1.0},  # Taux de distribution
        'profitability': {'range': (0, 50), 'weight': 2.0},  # Rentabilite
        'resultat_net': {'range': (0, 10), 'weight': 1.5},  # Resultat Net
        'capitalisation': {'range': (0, 1000), 'weight': 1.0},  # Capitalisation
        'long_term_debt_history': {'range': (0, 1000), 'weight': 1.5},  # Historical Dette
    }

    def __init__(self, stock):
        print(stock)
        self._fetcher = self.fetcher(stock)
        self._stock_name = stock
        
        assets = self._fetcher.get_total_actif()
        self._first_year_index = next(
            (index for index, value in enumerate(assets) if value != 0.0), None
        )
        self._last_year_index = next(
            (len(assets) - index - 1 for index, value in enumerate(assets[::-1]) if value != 0.0), None
        )

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
    def leverage_history(self):
        return self._leverage_history()

    @property
    def long_term_debt_history(self):
        return self._long_term_debt_history()

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
    def resultat_net(self):
        return self._net_income_history()

    @property
    def score(self):
        return self._score()

    # Analyze

    def bna_analyze(self):
        """TODO
        :return:
        """
        bna = self.bna
        value = "BNA "
        if bna == 0:
            value += "en decroissance. "
        elif bna == 1:
            value += "crois depuis l'annee precedente. "
        elif bna == 2:
            value += "en constante croissance: "
        value += "{}".format(self._fetcher.get_bpa())
        return value

    def bvps_analyze(self):
        """Verifie si BVPS < 0.7 * cours actuel
        Doit acheter a 0.7 * Cours actuel
        :return:
        """
        bvps = self.bvps
        value = "BVPS : prix reel de {}€".format(self._fetcher.get_book_value_share())
        if bvps == 0:
            value += " sur-evaluee "
        elif bvps == 1:
            value += " sous-evaluee "
        value += "par rapport a sa valeur reel."
        return value

    def cashflow_analyze(self):
        """Est-ce que CashFlow est positif
        :return:
        """
        cash = self._cash_flow
        value = "Tresorie: "
        if cash == 0:
            value += "negatif: "
        elif cash == 1:
            value += "positif: "
        value += "{:,.0f}M €".format(int(self._fetcher.get_cash_flow()) / 10 ** 6)
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
        value += history_data_to_string(self._fetcher.get_cash_flow_history())
        return value

    def ebitda_analyze(self):
        """Verifie si l EBITDA augmente au cours des 5 derniees annees.
        :return:
        """
        ebida = self.ebitda
        value = "EBITDA: Le Benefice Avant Interets, Impots, Depreciation et Amortissement "
        if ebida == 0:
            value += " est en baisse "
        elif ebida == 1:
            value += " crois depuis l annee precedente "
        elif ebida == 2:
            value += " en constante croissance "
        if not ebida:
            value += " aucune donnee."
        else:
            value += history_data_to_string(self._fetcher.get_ebitda_history())
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
            value += "sous-cote."
        elif per == 1:
            value += "normal."
        elif per == 2:
            value += "sur-cote."
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
        value += ": {:,.0f}M €".format(int(self._fetcher.get_capitalisation()) / 10 ** 6)
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

    def leverage_history_analyze(self):
        lev = self.leverage_history
        value = "Dette "
        if lev == 0:
            value += "en hausse: "
        elif lev == 1:
            value += "globalement en hausse: "
        elif lev == 2:
            value += "sans croissance particuliere: "
        elif lev == 3:
            value += "globalement en baisse: "
        elif lev == 4:
            value += "en baisse: "
        value += history_data_to_string(self._fetcher.get_debt_history())
        return value

    def long_term_debt_analyze(self):
        long_term = self.long_term_debt_history
        value = "Dette a long terme "
        if long_term == 0:
            value += "en hausse: "
        elif long_term == 1:
            value += "globalement en hausse: "
        elif long_term == 2:
            value += "sans croissance particuliere: "
        elif long_term == 3:
            value += "globalement en baisse: "
        elif long_term == 4:
            value += "en baisse: "
        value += history_data_to_string(self._fetcher.get_debt_long_history())
        return value

    def profitability_analyze(self):
        """Quel attractif une action specifique est par rapport a d autres actions.
        Plus le C/CF est bas, plus l action est evaluee meilleur marche.
        Rentabilite < 10
        :return:
        """
        prof = self.profitability
        value = "Rentabilite"
        if prof == 0:
            value += " pas rentable:"
        if prof == 1:
            value += " rentable:"
        value += " {}%".format(self._fetcher.get_profitability())
        value += " < 10%."
        return value

    def resultat_net_analyze(self):
        """Verifie si le resultat net augmente au cours des 5 dernieres annees.
        :return:
        """
        net_income = self.resultat_net
        value = "Resulat net {}".format(self._fetcher.get_profitability())
        if net_income == 0:
            value += " strictement decroissant: "
        if net_income == 1:
            value += " globalement decroissant: "
        if net_income == 2:
            value += " neutre: "
        if net_income == 3:
            value += " globalement croissant: "
        if net_income == 4:
            value += " strictement croissant: "
        value += history_data_to_string(self._fetcher.get_net_income_history())
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
            value += " crois depuis l'annee precedente: "
        if revenue == 2:
            value += " en constante croissance: "
        value += history_data_to_string(self._fetcher.get_revenue_history())
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
            value += " crois depuis l'annee precedente: "
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
        if price == 0:
            value += "faible "
        if price == 1:
            value += "assez faible "
        if price == 2:
            value += "neutre "
        if price == 3:
            value += "assez fort "
        if price == 4:
            value += "fort "

        value += "avec un rendement de : {}%".format(
            round((self._fetcher.get_dividend() / self._fetcher.get_price()) * 100, 2))
        value += " > 3%"
        return value

    def payout_ratio_analyze(self):
        """Taux de Distribution. Si le reverse trop de dividendes > 70%.
        :return:
        """
        payout = self.payout_ratio
        value = "Taux de Distribution des dividendes"
        if payout == 0:
            value += " trop eleve :"
        if payout == 1:
            value += " correct :"
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
            value += " strictement decroissant: "
        if price == 1:
            value += " globalement decroissant: "
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
        """Si le ROA est superieur a 10%.
        La societe genere assez de benefice avec ses actifs.
        :return:
        """
        roa = self.roa
        value = "ROA de"
        if roa == 0:
            value += " mauvaise rentabilite: "
        if roa == 1:
            value += " bonne rentabilite: "
        if roa == 2:
            value += " excellente rentabilite: "
        if roa == 3:
            value += " exceptionnel rentabilite: "

        value += "{}%".format(round(self._fetcher.get_roa(), 2))
        value += " > 10%"
        return value

    def roe_analyze(self):
        """Si le ROE est superieur a 10%.
        La societe genere assez de benefice avec ses actifs.
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

    def score_piotroski(self):
        """
            susceptibles de connaître des problemes financiers < 2
            Performance moyenne < 7
            surperformer les actions faibles de 7.5% par an sur une periode de 20 ans > 9
        :return:
        """
        assets = self._fetcher.get_total_actif()
        net_income = self._fetcher.get_net_income_history()
        roa = self._fetcher.get_roa()
        roa_hst = assets / assets.shift(1)
        cash_flow_from_ops = self._fetcher.get_cash_flow_operational()
        long_term_debt = self._fetcher.get_debt_long_history()
        current_liabilities = self._fetcher.get_total_passif_short_term()
        shares_outstanding = self._fetcher.get_shares_history()
        revenue = self._fetcher.get_revenue_history()
        cost_revenue = self._fetcher.get_cost_revenue()

        piotroski_score = 0

        # Critere 1: Revenu net positif
        if net_income.iloc[self._last_year_index] > 0:
            piotroski_score += 1

        # Critere 2: ROA positif
        if roa > 0:
            piotroski_score += 1

        # Critere 3: Cash Flow From Operations positif
        if cash_flow_from_ops.iloc[self._last_year_index] > 0:
            piotroski_score += 1

        # Critere 4: ROA est-il superieur a ROA de l annee precedente ?
        if roa_hst.iloc[self._last_year_index] > roa_hst.iloc[self._last_year_index-1]:
            piotroski_score += 1

        # Critere 5: Endettement a long terme est-il en baisse ?
        if long_term_debt.iloc[self._last_year_index] < long_term_debt.iloc[self._last_year_index-1]:
            piotroski_score += 1

        # Critere 6: Ratio de liquidite courante est-il en augmentation ?
        if(assets.iloc[self._last_year_index] / current_liabilities.iloc[self._last_year_index]) > \
                (assets.iloc[self._last_year_index-1] / current_liabilities.iloc[self._last_year_index-1]):
            piotroski_score += 1

        # Critere 7: Nombre d actions en circulation est-il en baisse
        if shares_outstanding.iloc[self._last_year_index] <= shares_outstanding.iloc[self._last_year_index-1]:
            piotroski_score += 1

        # Critere 8: Rentabilite brute est-elle positive
        gross_margin = (revenue - cost_revenue) / revenue
        if gross_margin.iloc[self._last_year_index] > 0:
            piotroski_score += 1

        # Critere 9: Cash Flow From Operations est-il superieur au revenu net ?
        if cash_flow_from_ops.iloc[self._last_year_index] > net_income.iloc[0]:
            piotroski_score += 1

        return piotroski_score

    def calculate_score(self):
        """
        Score sur 100%
        """
        return self.score.get("score_percent")

    def _score(self):
        """
        """
        per_param = {}
        total_note = 0
        total_max = 0

        for metric, max_val in self.MAX_SCORE.items():
            note = getattr(self, metric)

            # clamp note entre 0 et max_val pour eviter scores aberrants
            note_clamped = max(0, min(note, max_val))

            normalized = note_clamped / max_val if max_val > 0 else 0
            percent = round(normalized * 100, 2)

            per_param[metric] = {
                'note': note,
                'note_clamped': note_clamped,
                'max': max_val,
                'normalized': round(normalized, 4),
                'percent': percent
            }

            total_note += note_clamped
            total_max += max_val

        score_percent = round((total_note / total_max) * 100, 2) if total_max else 0.0
        score_10 = round((total_note / total_max) * 10, 2) if total_max else 0.0
        score_20 = round((total_note / total_max) * 20, 2) if total_max else 0.0

        return {
            'per_param': per_param,
            'total_note': total_note,
            'total_max': total_max,
            'score_percent': score_percent,
            'score_10': score_10,
            'score_20': score_20
        }

    def show(self):
        msg = [
            "Prix: {}€".format(self._fetcher.get_price()),
            self.bna_analyze(),
            self.bvps_analyze(),
            self.per_analyze(),
            self.capitalisation_analyze(),
            self.revenues_analyze(),
            self.resultat_net_analyze(),
            self.ebitda_analyze(),
            self.ebitda_marge_analyze(),
            self.cashflow_analyze(),
            self.cashflow_history_analyze(),
            self.leverage_analyze(),
            self.leverage_history_analyze(),
            self.long_term_debt_analyze(),
            self.dividends_analyze(),
            self.dividends_efficiancy_analyze(),
            self.payout_ratio_analyze(),
            self.profitability_analyze(),
            self.roa_analyze(),
            self.roe_analyze(),
            "{}%".format(self._score().get("score_percent"))
        ]

        print(f"📘 Recapitulatif action {self._stock_name} :")
        for k in msg:
            print(f" - {k}")

    def help_metrics(self, display: bool = True):
        """
        Retourne ou affiche les explications des indicateurs financiers utilises dans le bareme.
        :param display: si True, affiche un resume lisible ; sinon retourne seulement le dict
        """
        explanations = {
            "bna": "BNA (Benefice Net par Action) : benefice attribue a chaque action, indicateur de rentabilite par action.",
            "per": "PER (Price Earnings Ratio) : rapport entre le prix de l action et le benefice par action (BNA). "
                   "evalue combien d annees de benefices sont necessaires pour 'rembourser' le prix paye.",
            "roa": "ROA (Return on Assets) : rentabilite des actifs, mesure l efficacite de l entreprise a generer du profit avec ses actifs. Pour chaque euro investi combien de centimes de profit l'entreprise genere.",
            "roe": "ROE (Return on Equity) : rentabilite des fonds propres, mesure le rendement pour les actionnaires.",
            "bvps": "BVPS (Book Value Per Share) : valeur comptable par action (actifs nets / nombre d actions).",
            "capit": "Capitalisation : valeur totale de l entreprise en Bourse (prix de l action × nombre d actions).",
            "ebitda": "EBITDA (Earnings Before Interest, Taxes, Depreciation and Amortization) : benefice avant interêts, impôts, "
                      "amortissements. Sert a comparer la performance operationnelle.",
            "cashflow": "Cash Flow (flux de tresorerie) : liquidites generees par l activite, indicateur de solidite financiere.",
            "revenues": "Revenues (Chiffre d affaires) : total des ventes realisees sur une periode donnee.",
            "leverage": "Leverage (effet de levier / endettement) : mesure du poids de la dette par rapport aux fonds propres.",
            "dividends": "Dividendes : part du benefice distribuee aux actionnaires.",
            "payout_ratio": "Payout Ratio (taux de distribution) : pourcentage du benefice distribue en dividendes.",
            "profitability": "Profitabilite : capacite globale de l entreprise a generer du profit sur ses ventes et capitaux.",
            "resultat_net": "Resultat Net : benefice final apres impôts, charges financieres et exceptionnelles.",
        }

        if display:
            print("📘 Explications des indicateurs financiers :")
            for k, v in explanations.items():
                print(f" - {k.upper()}: {v}")

        return explanations


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

        # Securiser les index
        self._first_year_index = min(self._first_year_index, len(series_data) - 1)
        self._last_year_index = min(self._last_year_index, len(series_data) - 1)

        fully_increase = all(i < j for i, j in zip(series_data[self._first_year_index:self._last_year_index], series_data[2:]))
        fully_decrease = all(i > j for i, j in zip(series_data[self._first_year_index:self._last_year_index], series_data[2:]))
        if fully_decrease:
            value = 0
        elif fully_increase:
            value = 4
        elif series_data[self._first_year_index] > series_data[self._last_year_index]:
            value = 1
        elif series_data[self._first_year_index] < series_data[self._last_year_index]:
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

    def _leverage_history(self):
        debt = self._fetcher.get_debt_history()
        series_data = []
        last_year = None
        for year, group in debt.groupby(debt.index.year):
            for i in group:
                if last_year != year:
                    last_year = year
                    series_data.append(i)

        self._first_year_index = next((index for index, value in enumerate(series_data) if value != 0.0), None)

        fully_increase = all(i < j for i, j in zip(series_data[self._first_year_index:self._last_year_index], series_data[2:]))
        fully_decrease = all(i > j for i, j in zip(series_data[self._first_year_index:self._last_year_index], series_data[2:]))
        if fully_decrease:
            value = 4
        elif fully_increase:
            value = 0
        elif series_data[self._first_year_index] > series_data[self._last_year_index]:
            value = 3
        elif series_data[self._first_year_index] < series_data[self._last_year_index]:
            value = 1
        else:
            value = 2
        return value

    def _long_term_debt_history(self):
        long_term_debt = self._fetcher.get_debt_long_history()
        series_data = []
        last_year = None

        if long_term_debt.empty:
            return 0

        for year, group in long_term_debt.groupby(long_term_debt.index.year):
            for i in group:
                if last_year != year:
                    last_year = year
                    series_data.append(i)

        self._first_year_index = min(self._first_year_index, len(series_data) - 1)
        self._last_year_index = min(self._last_year_index, len(series_data) - 1)

        fully_increase = all(
            i < j for i, j in zip(series_data[self._first_year_index:self._last_year_index], series_data[2:]))
        fully_decrease = all(
            i > j for i, j in zip(series_data[self._first_year_index:self._last_year_index], series_data[2:]))
        if fully_decrease:
            value = 0
        elif fully_increase:
            value = 4
        elif series_data[self._first_year_index] > series_data[self._last_year_index]:
            value = 1
        elif series_data[self._first_year_index] < series_data[self._last_year_index]:
            value = 3
        else:
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
            value = 0
        elif 0 < rendement < 1:
            value = 1
        elif 1 < rendement < 2:
            value = 2
        elif 2 < rendement < 3:
            value = 3
        else:
            value = 4

        return value

    def _bna_history(self):
        bna = self._fetcher.get_bpa_history()
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
        if roa <= 3:
            value = 0
        if 5 < roa < 10:
            value = 1
        if 10 < roa < 15:
            value = 2
        if roa >= 15:
            value = 3
        return value

    def _roa_history(self):
        assets = self._fetcher.get_total_actif()
        roa_hst = (assets / assets.shift(1)).fillna(0)
        value = 0
        return value

    def _roe(self):
        roe = self._fetcher.get_roe()
        value = 0
        if roe >= 10:
            value = 1
        return value



if __name__ == "__main__":
    # analyze = Analyzer("STLAP.PA")
    analyze = Analyzer("MSFT")
    # print("per  ", analyze.per)
    # print("bvps ", analyze.bvps)
    # print("leverage ", analyze.leverage_history_analyze())
    # print("dividend ", analyze.dividends_efficiancy_analyze())
    # print("cashflow_history ", analyze._net_income_history())
    # print("cashflow_history ", analyze.cashflow_history_analyze())
    # print("price ", analyze.price_analyze())
    # print("resultat net ", analyze.resultat_net_analyze())
    # print("capit", analyze.capitalisation)
    # print("chiffre affaire", analyze.revenues)
    # print("dividendes", analyze.dividends)
    # print("bna", analyze.bna)
    # pprint(analyze.long_term_debt_analyze())
    # print("payout_ratio", analyze.payout_ratio, analyze.payout_ratio_analyze())
    pprint(analyze.score)
    analyze.show()
    # pprint(analyze.score_piotroski())
    # pprint(analyze.calculate_level())
    quit()
    actions = [
        "STLAP.PA",
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
        break
