

def getOrderRateLimits(recvWindow = 1000):
    reqInfo = basicOrderDataShell();
    reqInfo['parameters']['recvWindow'] = recvWindow
    reqInfo['weight'] = 20
    reqInfo['endpoint_uri'] = '/api/v3/rateLimit/order'
    return reqInfo

def getMyOrderStatus(orderId = None, base = 'BTC', quote = 'USD', recvWindow = 1000):
    symbol = base + quote
    reqInfo = basicOrderDataShell();
    reqInfo['parameters']['recvWindow'] = recvWindow
    reqInfo['parameters']['symbol'] = symbol
    reqInfo['parameters']['orderId'] = orderId
    reqInfo['weight'] = 2
    reqInfo['endpoint_uri'] = '/api/v3/order'
    reqInfo['source'] = 'database'
    return reqInfo

def getOpenOrders(base = 'BTC', quote = 'USD', recvWindow = 1000):
    symbol = base + quote
    reqInfo = basicOrderDataShell();
    reqInfo['parameters']['recvWindow'] = recvWindow
    reqInfo['parameters']['symbol'] = symbol
    reqInfo['weight'] = 3
    reqInfo['endpoint_uri'] = '/api/v3/openOrders'
    reqInfo['source'] = 'database'
    return reqInfo

def getMyTrades(base = 'BTC', quote = 'USD', fromId = 0, orderId = 0, startTime = 0, endTime = 0, limit = 10, recvWindow = 1000):
    symbol = base + quote
    reqInfo = basicOrderDataShell();
    reqInfo['parameters']['recvWindow'] = recvWindow
    reqInfo['parameters']['symbol'] = symbol
   # reqInfo['parameters']['limit'] = limit
    reqInfo['weight'] = 10
    reqInfo['endpoint_uri'] = '/api/v3/myTrades'
    reqInfo['source'] = 'database'
    reqInfo['optionalParameters']['fromId'] = fromId
    reqInfo['optionalParameters']['orderId'] = orderId
    reqInfo['optionalParameters']['startTime'] = startTime
    reqInfo['optionalParameters']['endTime'] = endTime
    return reqInfo


def basicOrderDataShell():
    return {
        'type': 'DATA',
        'endpointType': 'GET',
        'endpoint_uri': '',
        'security': 'signed',
        'max_recvWindow': 60000,
        'weight': 1,
        'source': 'memory',
        'parameters': {},
        'optionalParameters': {}
    }
