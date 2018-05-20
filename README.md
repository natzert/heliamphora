## Introduction

This is a rewrite of heliamphora using golang. I mostly just got bored and decided to give go a shot. This is a mostly complete rewrite of heliamorpha except that, at the time of writing, it only supports USD. The config syntax has changed a bit too. The python version uses an ini style, this one uses yaml or json. Whichever you prefer.

Also, this seems to be about 75% faster than the python version so I'm very happy with that.

![Example output heliamphora](https://i.imgur.com/hjVXWCj.png)

## Installation

To build this you'll need the following packages:

github.com/bclicn/color
github.com/olekukonko/tablewriter
github.com/spf13/viper

## Configuration

The config file has been moved to `~/.heli.yaml`. Here is an example configuration:

```
balances:
  bitcoin: 1.12345678
  ethereum: 1.12345678
  litecoin: 1.12345678
  ripple: 1.12345678
  nano: 1.12345678
general:
  invested: -500
  fiat_currency: USD
```

You can get a full list of available crypto currencies on coinmarketcap.com or by running this command and looking at the `id` fields (requires [jq](https://stedolan.github.io/jq/)):

```
curl https://api.coinmarketcap.com/v1/ticker/ | jq .[].id
```
