#!/usr/bin/python3

import argparse,json,os,re,socket,sys,urllib.request

def init_argparse():
    parser = argparse.ArgumentParser(description='convert cryptocurrencies conveniently.', usage=os.path.basename(sys.argv[0]) + ' amount [currency] [-p ...]')

    parser.add_argument('amount', help='coin amount to convert', default=None)
    parser.add_argument('currency', nargs='?', help='specify currency -- default is btc', default='btc')
    parser.add_argument('--perform', '-p', help='which conversions to perform -- eg. gbp,eur,usd', default=None)

    args = parser.parse_args()
    args = vars(args)

    try:
        args['amount'] = float(args['amount'])
    except:
        print('error: amount must be an int or float.')
        sys.exit(1)

    args['currency'] = args['currency'].upper()

    if args['perform'] is not None:
        perform = []
        for p in args['perform'].split(','):
            perform.append(p.upper())
        args['perform'] = perform

    return args

def blockchain_api(method='ticker', currency=None, amount=None):
    response = None

    try:
        socket.setdefaulttimeout(30)
        if method == 'ticker':
            url = 'https://blockchain.info/ticker'
        elif method == 'tobtc' and currency is not None and amount is not None:
            url = 'https://blockchain.info/tobtc?currency=%s&value=%s' % (currency, amount)

        response = urllib.request.urlopen(url).read().decode('utf-8')

    except:
        print('error: unable to connect to blockchain.info api.')
        sys.exit(1)

    return response

def print_crypto(currency, amount):
    print('        %s: %s' % (currency, re.sub('\.?0+$', '', str(amount))))
    print('       m%s: %s' % (currency, re.sub('\.?0+$', '', str(amount * 1000))))
    print('       μ%s: %s' % (currency, re.sub('\.?0+$', '', str(amount * 1000000))))
    if currency == 'BTC':
        print('    satoshi: %s' % (re.sub('\.?0+$', '', str(amount * 100000000))))
    else:
        print('   smallest: %s' % (re.sub('\.?0+$', '', str(amount * 100000000))))
    print('')

def main(args):
    amount = args['amount']
    currency = args['currency']
    perform = args['perform']

    cryptocurrencies = ['BTC']
    if currency not in cryptocurrencies:
        tobtc = blockchain_api('tobtc', currency, amount)
        print_crypto('BTC', float(tobtc))

        return True

    print_crypto(currency, amount)

    ticker = json.loads(blockchain_api('ticker'))
    for row in ticker:
        if perform is not None and row not in perform:
            continue
        print(' [%s]\t%s: %s' % (ticker[row]['symbol'], row, (amount * ticker[row]['15m'])))

if __name__ == '__main__':
    args = init_argparse()
    if main(args) == False:
        sys.exit(1)
