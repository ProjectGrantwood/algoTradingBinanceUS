import utils
import requests
import binanceus_signature as buss
from binance.spot import Spot
from binance.websocket.spot.websocket_client import SpotWebsocketClient as wsclient
from api_access import key, secret

requests.packages.urllib3.util.connection.HAS_IPV6 = False # see explanation below

# If you've restricted use of your API key to specific IP addresses on the API key page of your BinanceUS account, you only have the option to provide it in IPv4 format. 

# However, the requests library utilizes a package that seems to assume you're using the IPv6 format when making API calls. (Ham-headed optimism, general oversight, or...?)

# Other solutions include checks, check out https://stackoverflow.com/questions/33046733/force-requests-to-use-ipv4-ipv6
    
def create_websocket_client():
    client = wsclient(stream_url='wss://stream.binance.us:9443')
    return client

def key_access_client(api_key):
    client = Spot(key=api_key, base_url='https://api.binance.us')
    return client

async def secureDelete(shellObject = {}, api_key = key, api_sec = secret, return_query = False):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = buss.sign(shellObject['parameters'], api_sec)
    payload = {
        **shellObject['parameters'],
        "signature": signature
    }
    req = requests.delete(("https://api.binance.us" + shellObject['endpoint_uri']), headers = headers, params = payload)
    if return_query == False:
        return req
    return {'response': req, 'query_details': shellObject, 'request': req.request}

async def securePost(shellObject = {}, api_key, api_sec, return_query = False):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = buss.sign(shellObject['parameters'], api_sec)
    payload = {
        **shellObject['parameters'],
        "signature": signature
    }
    req = requests.post(("https://api.binance.us" + shellObject['endpoint_uri']), headers = headers, data = payload)
    if return_query == False:
        return req
    return {'response': req, 'query_details': shellObject, 'request': req.request}

async def secureGet(shellObject = {}, api_key, api_sec, return_query = False):
    req = headers = {}
    headers['X-MBX-APIKEY'] = api_key
    
    signature = buss.sign(shellObject['parameters'], api_sec)
    payload = {
        **shellObject['parameters'],
        "signature": signature,
    }
    req = requests.get(("https://api.binance.us" + shellObject['endpoint_uri']), headers = headers, params = payload)
    if return_query == False:
        return req
    return {'response': req, 'query_details': shellObject, 'request': req.request}

async def keyedGet(shellObject = {}, api_key, paramsInQueryString = True, return_query = False):
    req = headers = {}
    headers['X-MBX-APIKEY'] = api_key
    queryString = "https://api.binance.us" + shellObject['endpoint_uri']
    if paramsInQueryString == False:
        payload = {
            **shellObject['parameters']
        }
        req = requests.get(queryString, headers = headers, data = payload)
    if paramsInQueryString == True:
        queryString += '?'
        k = shellObject['parameters'].keys()
        initialParameter = True
        for i in k:
            if initialParameter == False:
                queryString += '&'
            initialParameter = False
            queryString += i
            queryString += '='
            queryString += str(shellObject['parameters'][i])
        req = requests.get(queryString, headers = headers)
    if return_query == False:
        return req
    return {'response': req, 'query_details': shellObject, 'request': req.request}

async def get(shellObject = {}, paramsInQueryString = True, return_query = False):
    req = {}
    queryString = "https://api.binance.us" + shellObject['endpoint_uri']
    if paramsInQueryString == False:
        payload = {
            **shellObject['parameters']
        }
        req = requests.get(queryString, data = payload)
    if paramsInQueryString == True:
        queryString += '?'
        k = shellObject['parameters'].keys()
        initialParameter = True
        for i in k:
            if initialParameter == False:
                queryString += '&'
            initialParameter = False
            queryString += i
            queryString += '='
            queryString += str(shellObject['parameters'][i])
        req = requests.get(queryString)
    if return_query == False:
        return req
    return {'response': req, 'query_details': shellObject, 'request': req.request}

async def add_timestamp(shellObject, statusCode1021 = False):
    shellObject['parameters']['timestamp'] = utils.get_time()
    if statusCode1021 == True:
        shellObject['parameters']['timestamp'] = shellObject['parameters']['timestamp'] - 1000
    return shellObject