
def pingServer():
    reqInfo = basicDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/ping'
    return reqInfo

def serverTime():
    reqInfo = basicDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/time'
    return reqInfo

def systemStatus():
    reqInfo = basicDataShell()
    reqInfo['endpoint_uri'] = '/sapi/v1/system/status'
    reqInfo['security'] = 'signed'
    return reqInfo

def getTradingPairInfo():
    reqInfo = basicDataShell()
    reqInfo['endpoint_uri'] = '/api/v3/exchangeInfo'
    reqInfo['weight'] = 10
    return reqInfo


def basicDataShell():
    return {
        'type': 'DATA',
        'endpointType': 'GET',
        'endpoint_uri': '',
        'security': 'none',
        'weight': 1,
        'source': 'memory',
        'parameters': {
            
        }
    }