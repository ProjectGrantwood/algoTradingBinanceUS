import binanceus_request as busr

def getTrades(base = 'BTC', quote = 'USD', limit = 10):
    basicShell = basicTradeDataShell(base, quote, limit)
    basicShell['endpoint_uri'] += 'trades'
    basicShell['parameters']['limit'] = limit
    basicShell['source'] = 'memory'
    return basicShell

def getHistoricalTrades(base = 'BTC', quote = 'USD', limit = 10, startTime = None, endTime = None):
    basicShell = basicTradeDataShell(base, quote, limit)
    basicShell['endpoint_uri'] += 'historicalTrades'
    basicShell['weight'] = 5
    basicShell['security'] = 'keyed'
    basicShell['parameters']['limit'] = limit
    if startTime != None and endTime != None:
        basicShell['parameters']['startTime'] = startTime
        basicShell['parameters']['endTime']
    return basicShell

def getAggregateTrades(base = 'BTC', quote = 'USD', limit = 10, fromId = 0, startTime = 0, endTime = 0):
    basicShell = basicTradeDataShell(base, quote, limit)
    basicShell['endpoint_uri'] += "aggTrades"
    if startTime != None and endTime != None:
        basicShell['parameters']['startTime'] = startTime
        basicShell['parameters']['endTime']
    if fromId != None:
        basicShell['parameters']['fromId'] = fromId
    return basicShell

def getDepth(base = 'BTC', quote = 'USD', limit = 100, fromId = None, startTime = None, endTime = None):
    basicShell = basicTradeDataShell(base, quote, limit)
    basicShell['endpoint_uri'] += "depth"
    basicShell['source'] = 'memory'
    basicShell['weight'] = getDepthWeight(limit)
    basicShell['max_limit'] = 5000
    if startTime != None and endTime != None:
        basicShell['parameters']['startTime'] = startTime
        basicShell['parameters']['endTime']
    if fromId != None:
        basicShell['parameters']['fromId'] = fromId
    return basicShell

def getKlines(base = 'BTC', quote = 'USD', limit = 100, interval = '1m', startTime = None, endTime = None, fromId = None):
    basicShell = basicTradeDataShell(base, quote, limit)
    basicShell['endpoint_uri'] += 'klines'
    basicShell['parameters']['interval'] = interval

    if startTime != None and endTime != None:
        basicShell['parameters']['startTime'] = startTime
        basicShell['parameters']['endTime']
    if fromId != None:
        basicShell['parameters']['fromId'] = fromId
    return basicShell

def basicTradeDataShell(base = 'BTC', quote = 'USD', limit = '5'):
    symbolString = base + quote
    return {
        'type': 'DATA',
        'endpointType': 'GET',
        'endpoint_uri': '/api/v3/',
        'max_limit': 1000,
        'weight': 1,
        'source': 'database',
        'security': 'none',
        'parameters': {
            'symbol': symbolString,
            'limit': limit
        },
        'optionalParameters': {}
    }

def getDepthWeight(limit):
    weight = 1
    if limit > 101:
        weight += 4 #5 in total
    if limit > 501:
        weight += 5 #10 in total
    if limit > 1001:
        weight += 40 #50 in total
    return weight