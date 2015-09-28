coinversion
=====

coinversion prints any given bitcoin value in an array of currencies and denominations -- and vice versa.

* tidy, minimal, command line interface
* uses blockchain.info API -- [blockchain]

## dependencies:
* Python3

## usage:
* coinversion.py amount [currency] \[-p ...\]

## examples:
* `coinversion.py 1.5` -- will print value of 1.5 bitcoin in all supported currencies
* `coinversion.py 148.18 gbp` -- will print value of 148.18 GBP in bitcoin
* `coinversion.py 9 -p gbp` -- will print value of 9 bitcoin in GBP

[blockchain]: https://blockchain.info/api
