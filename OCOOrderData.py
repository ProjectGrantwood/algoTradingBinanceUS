def getOCOOrderStatus(orderListId = None, base = 'BTC', quote = 'USD', recvWindow = 1000):
    symbol = base + quote
    reqInfo = basicOCOOrderDataShell();
    reqInfo['parameters']['recvWindow'] = recvWindow
    reqInfo['parameters']['symbol'] = symbol
    reqInfo['parameters']['orderListId'] = orderListId
    reqInfo['weight'] = 2
    reqInfo['endpoint_uri'] = '/api/v3/orderList'
    reqInfo['source'] = 'database'
    return reqInfo

def getOpenOCOOrders(base = 'BTC', quote = 'USD', recvWindow = 1000):
    symbol = base + quote
    reqInfo = basicOCOOrderDataShell();
    reqInfo['parameters']['recvWindow'] = recvWindow
    reqInfo['parameters']['symbol'] = symbol
    reqInfo['weight'] = 3
    reqInfo['endpoint_uri'] = '/api/v3/openOrderList'
    reqInfo['source'] = 'database'
    return reqInfo

def getOCOOrders(base = 'BTC', quote = 'USD', fromId = 0, orderId = 0, startTime = 0, endTime = 0, limit = 10, recvWindow = 1000):
    symbol = base + quote
    reqInfo = basicOCOOrderDataShell();
    reqInfo['parameters']['recvWindow'] = recvWindow
    reqInfo['parameters']['symbol'] = symbol
    reqInfo['weight'] = 10
    reqInfo['endpoint_uri'] = '/api/v3/allOrderList'
    reqInfo['source'] = 'database'
    reqInfo['optionalParameters']['fromId'] = fromId
    reqInfo['optionalParameters']['orderId'] = orderId
    reqInfo['optionalParameters']['startTime'] = startTime
    reqInfo['optionalParameters']['endTime'] = endTime
    reqInfo['parameters']['limit'] = limit
    return reqInfo


def basicOCOOrderDataShell():
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
