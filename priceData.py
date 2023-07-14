def getTickerPrice(base = 'BTC', quote = 'USD'):
    symbol = base + quote
    reqInfo = basicPriceDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/ticker/price'
    reqInfo['parameters']['symbol'] = symbol
    return reqInfo

def getAveragePrice(base = 'BTC', quote = 'USD'):
    symbol = base + quote
    reqInfo = basicPriceDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/avgPrice'
    reqInfo['parameters']['symbol'] = symbol
    return reqInfo

def getBestOrderBookPrice(base = 'BTC', quote = 'USD'):
    symbol = base + quote
    reqInfo = basicPriceDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/ticker/bookTicker'
    reqInfo['parameters']['symbol'] = symbol
    return reqInfo

def get24hrChange(base = 'BTC', quote = 'USD'):
    symbol = base + quote
    reqInfo = basicPriceDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/ticker/24hr'
    reqInfo['parameters']['symbol'] = symbol
    return reqInfo

def getRollingWindowChange(base = 'BTC', quote = 'USD', windowSize = '1m'):
    symbol = base + quote
    reqInfo = basicPriceDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/ticker'
    reqInfo['source'] = 'database'
    reqInfo['weight'] = 2
    reqInfo['parameters']['windowSize'] = windowSize
    reqInfo['parameters']['symbol'] = symbol
    return reqInfo


def basicPriceDataShell():
    return {
        'type': 'DATA',
        'endpointType': 'GET',
        'endpoint_uri': '',
        'security': 'none',
        'weight': 1,
        'source': 'memory',
        'parameters': {},
        'optionalParameters': {}
    }
    
