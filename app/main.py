#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes

from pprint import pprint
import yfinance as yf

stcks = yf.Ticker("MSFT")
print(stcks.info)
# print("")
# pprint(stcks.actions)
# print("")
# pprint(stcks.dividends)
# print("")
# pprint(stcks.splits)
# print("")
# pprint(stcks.capital_gains)
# print("")
# pprint(stcks.get_shares_full(start="2022-01-01", end=None))

# show financials:
# - income statement
# print(stcks.income_stmt)
# print("")
# print(stcks.quarterly_income_stmt)
# print("")


# - balance sheet
# print(stcks.balance_sheet)
# print("")
# print(stcks.quarterly_balance_sheet)
# print("")
#
# # - cash flow statement
# print(stcks.cashflow)
# print("")
# print(stcks.quarterly_cashflow)
# print("")
# # see `Ticker.get_income_stmt()` for more options
#
# # show holders
# print("")
# print(stcks.major_holders)
# print("")
# print(stcks.institutional_holders)
# print("")
# print(stcks.mutualfund_holders)
#
# # Show future and historic earnings dates, returns at most next 4 quarters and last 8 quarters by default.
# # Note: If more are needed use msft.get_earnings_dates(limit=XX) with increased limit argument.
# print("")
# print(stcks.earnings_dates)
#
# # show ISIN code - *experimental*
# # ISIN = International Securities Identification Number
# print("")
# print(stcks.isin)
#
# # show options expirations
# print("")
# print(stcks.options)
# # show news
# print("")
# print(stcks.news)