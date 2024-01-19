#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import pandas as pd


class DataToDict(object):

    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return self._data.to_string()

    def append(self, data):
        result = self._data.append(data)
        self._data = result.fillna(0)

    def get(self, key, default=None):
        if key not in self._data.index:
            return default
        return self._data.loc[key]

    def keys(self):
        return self._data
