#!/usr/bin/env python

import os
import sys
import requests
import json
import ConfigParser
from tabulate import tabulate
from termcolor import colored

class Parser(ConfigParser.ConfigParser):
  def as_dict(self):
    d = dict(self._sections)
    for k in d:
      d[k] = dict(self._defaults, **d[k])
      d[k].pop('__name__', None)
    return d

p = Parser()
p.read(os.path.expanduser('~/.heliamphora'))
input_data = p.as_dict()
balances = input_data['balances']
invested = float(input_data['general']['invested'])
fiat_currency = input_data['general']['fiat_currency']
api_key = input_data['general']['api_key']

totals = []
final_data = []

def trend_format(input):
  if str(input).startswith("-"):
    return colored(input, 'red')
  else:
    return colored(input, 'green')

def coin_index(list, key, value):
  for i, dic in enumerate(list):
    if dic[key] == value:
      return i
  return -1

def price_calc():
  headers = {'X-CMC_PRO_API_KEY': api_key}
  coin_data = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert={0}'.format('USD'), headers=headers)
  coin_dict = coin_data.json()

  last_dict_effort = {}
  last_dict_effort['data'] = []

  for coin, ammount in balances.items():
    index = coin_index(coin_dict['data'], "slug", coin)
    last_dict_effort['data'].append(coin_dict['data'][index])

    cur_price = coin_dict['data'][index]['quote']['USD']['price']
    value = float(ammount) * float(cur_price)
    totals.append(value)

    hour = trend_format(coin_dict['data'][index]['quote']['USD']['percent_change_1h'])
    day = trend_format(coin_dict['data'][index]['quote']['USD']['percent_change_24h'])
    week = trend_format(coin_dict['data'][index]['quote']['USD']['percent_change_7d'])

    final_data.append([coin, cur_price, ammount, value, hour, day, week])

def total_value():
  sum = 0
  for x in totals:
    sum += x
  return sum

price_calc()

final_data.append([None, None])
final_data.append(['Gross', None, None, total_value()])
final_data.append(['Exp', None, None, invested])
final_data.append(['Net', None, None, trend_format(str(total_value() + invested))])

print tabulate(final_data, headers=[
        'Coin',
        'Price',
        'Amount',
        'Balance',
        '1h',
        '1d',
        '1w'
    ],
    floatfmt=(
        ".2f",
        ".2f",
        ".8f",
        ".2f",
        ".2f",
        ".2f",
        ".2f"
    )
    )

print
print "All prices displayed in {0}".format(fiat_currency)
print "Prices sourced from https://coinmarketcap.com"
