#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

class DataToDict(object):

    def __init__(self, data):
        self._data = data

    def __repr__(self):
        return self._data.to_string()

    def get(self, key):
        return self._data.loc[key]

    def keys(self):
        return self._data
