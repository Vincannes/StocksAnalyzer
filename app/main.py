#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

import json
import os
from pprint import pprint
from app.core.analyzer import Analyzer

data = {}
with open("datas/cac40.json", 'r') as files:
    data = json.load(files)
# pprint(data)

THIS_DIR = os.path.dirname(__file__)
export_path = os.path.join(THIS_DIR, "datas", "analyze_cac40.json")


def all_cac():
    scores = {}
    for name, code in data.items():
        stock = Analyzer(code)
        lvl = stock.calculate_score()
        scores[name] = (lvl, stock.show())

    dictionnaire_trie = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)
    pprint(dictionnaire_trie)

    with open(export_path, "w") as file:
        json.dump(dictionnaire_trie, file, indent=4)


def action(code):
    stock = Analyzer(code)
    lvl = stock.calculate_score()
    stock.help_metrics()
    stock.show()
    print(lvl)


# action(data.get("Pernod Ricard"))
action(data.get("TotalEnergies"))
# action(data.get("Lvmh"))
# action(data.get("Bnp Paribas"))
# all_cac()


# a ajouter
# La société distribue un dividende de 3,16 € pour un rendement annualisé de 6.11%.
# https://rendementbourse.com/fp-total

