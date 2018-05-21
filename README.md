## Introduction

Heliamphora is for calculating the value of your crypto currencies. You tell it how much of any given crypto currency you have and it will calculate the current value in fiat.

![Example output heliamphora](https://i.imgur.com/jtNBrpC.png)

## Installation

This script requires the following python libraries:

* requests
* tabulate
* termcolor

## Configuration

Copy the `.heliamphora.example` file to `$HOME/.heliamphora` and edit the appropriate values for your crypto.

You can get a full list of available crypto currencies on coinmarketcap.com or by running this command and looking at the `id` fields (requires [jq](https://stedolan.github.io/jq/)):

```
curl https://api.coinmarketcap.com/v1/ticker/ | jq .[].id
```

The `fiat_currency` option under the general section is the currency that your crypto will be calculated against. Available values are:
```
AUD
BRL
CAD
CHF
CLP
CNY
CZK
DKK
EUR
GBP
HKD
HUF
IDR
ILS
INR
JPY
KRW
MXN
MYR
NOK
NZD
PHP
PKR
PLN
RUB
SEK
SGD
THB
TRY
TWD
USD
ZAR
```
