

def getAccount(recvWindow=1000):
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/account'
    reqInfo['weight'] = 10
    reqInfo['parameters']['recvWindow'] = recvWindow
    return reqInfo

def getAccountStatus(recvWindow=1000):
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v3/accountStatus'
    reqInfo['parameters']['recvWindow'] = recvWindow
    return reqInfo

def getAPITradingStatus(recvWindow=1000):
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v3/apiTradingStatus'
    return reqInfo

def getAssetDistributionHistory(recvWindow=1000):
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v1/asset/assetDistributionHistory'
    reqInfo['parameters']['recvWindow'] = recvWindow
    return reqInfo

def getSpotOrderSnapshot(recvWindow=1000):
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v1/accountSnapshot'
    reqInfo['parameters']['type'] = 'SPOT'
    reqInfo['parameters']['recvWindow'] = recvWindow
    return reqInfo

def getTradingFees(base='BTC', quote='USD', recvWindow=1000):
    symbol = base + quote
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v1/asset/query/trading-fee'
    reqInfo['parameters']['symbol'] = symbol
    reqInfo['parameters']['recvWindow'] = recvWindow
    return reqInfo

def get30DayTradingVolume(recvWindow=1000):
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v1/asset/query/trading-volume'
    reqInfo['parameters']['recvWindow'] = recvWindow
    return reqInfo

def getAssets(recvWindow=1000):
    reqInfo = basicUserDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v1/capital/config/getall'
    reqInfo['parameters']['recvWindow'] = recvWindow
    return reqInfo
    
def basicUserDataShell():
    return {
        'type': 'DATA',
        'endpointType': 'GET',
        'endpoint_uri': '',
        'max_recvWindow': 60000,
        'weight': 1,
        'source': 'database',
        'security': 'signed',
        'parameters': {},
        'optionalParameters': {}
    }