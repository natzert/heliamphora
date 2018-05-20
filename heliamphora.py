#!/usr/bin/env python

import os
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

totals = []
final_data = []

def trend_format(input):
  if input.startswith("-"):
    return colored(input, 'red')
  else:
    return colored(input, 'green')

def price_calc(currency, amount):
  coin_data = requests.get('https://api.coinmarketcap.com/v1/ticker/{0}/?convert={1}'.format(currency, fiat_currency))
  coin_dict = json.loads(coin_data.text)
  price_key = 'price_{0}'.format(fiat_currency.lower())

  cur_price = coin_dict[0][price_key]
  value = float(ammount) * float(cur_price)
  totals.append(value)

  hour = trend_format(coin_dict[0]['percent_change_1h'])
  day = trend_format(coin_dict[0]['percent_change_24h'])
  week = trend_format(coin_dict[0]['percent_change_7d'])

  final_data.append([currency, cur_price, ammount, value, hour, day, week])

def total_value():
  sum = 0
  for x in totals:
    sum += x
  return sum

for currency, ammount in sorted(balances.iteritems(), key=lambda (k,v): (v,k)):
  price_calc(currency, ammount)

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
