#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

import json
from pprint import pprint
from app.core.analyzer import Analyzer

data = {}
with open("datas/cac40.json", 'r') as files:
    data = json.load(files)


def all_cac():
    scores = {}
    for name, code in data.items():
        stock = Analyzer(code)
        lvl = stock.calculate_level()
        scores[name] = lvl

    dictionnaire_trie = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    pprint(dictionnaire_trie)


def action(code):
    stock = Analyzer(code)
    lvl = stock.calculate_level()
    msg = stock.show()
    pprint(msg)
    print(lvl)


action(data.get("Pernod Ricard"))
print()
# action(data.get("Lvmh"))
