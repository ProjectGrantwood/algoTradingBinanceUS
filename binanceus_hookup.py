# Wrapper module for sending requests

import binanceus_request as busr
from utils import num_out

# Below is a generic send function for all types of endpoints and requests included in this library. 
# All individual functions (listed in functionList.txt) will return a dict object which you use as the single parameter. 
# Authentication, headers, and other types of checks are performed for you. 
# Return value is the response from the BinanceUS API. 
# You can optionally enable the return of the dict object you supplied as a parameter, as well... 
# although I don't recommend this for any robust trading application (milliseconds matter!)

async def select_send(req, return_query):
    if req['endpointType'] == 'POST':
        if req['pre_request_information']['status'] != 'SIGN':
            return req['pre_request_information']['message']
        response = await busr.securePost(req, return_query = return_query)
        return response
    if req['endpointType'] == 'DELETE':
        if req['pre_request_information']['status'] != 'SIGN':
            return req['pre_request_information']['message']
        response = await busr.secureDelete(req, return_query = return_query)
        return response
    if req['endpointType'] == 'GET':
        if req['security'] == 'signed':
            response = await busr.secureGet(req, return_query = return_query)
            return response
        if req['security'] == 'none':
            response = await busr.get(req, return_query = return_query)
            return response
        if req['security'] == 'keyed':
            response = await busr.keyedGet(req, return_query = return_query)
            return response
    print("Send Failure, check parameters")
    return False
        
async def send(req, return_query = False, recvWindowOverride = None):
    if recvWindowOverride != None:
        req['parameters']['recvWindow'] = recvWindowOverride
    if req['security'] == 'signed' or req['security'] == 'keyed':
        req = await busr.add_timestamp(req, False)
    response = await select_send(req, return_query)
    statuscode = None
    if return_query == True:
        statuscode = response['response'].status_code
    else:
        statuscode = response.status_code
    if statuscode == 200:
        return response
    if statuscode == 400:
        js = None
        if return_query == True:
            js = response['response'].json()
        else: 
            js = response.json()
        if js['code'] == -1021:
            req = await busr.add_timestamp(req, True)
            response = await select_send(req, return_query)
        else:
            return response

async def quickSend(func, dictOfParams = None, return_query = False, recvWindowOverride = None):
    if dictOfParams != None:
        req = func(**dictOfParams)
        resp = await send(req, return_query, recvWindowOverride)
        return resp
    else:
        req = func()
        resp = await send(req, return_query, recvWindowOverride)
        return resp

async def quickRead(func, dictOfParams = None):
    response = await quickSend(func, dictOfParams, False)
    response = num_out(response.json())
    print(response)
    return response

# A function for sending test orders to the API that will accept the results of any ordering function in the order or orderOCO modules without A) copying the entire object or B) permanently mutate the object's 'endpoint_uri' entry.

async def testOrder(orderShellObject, return_query = True):
    original_endpoint = orderShellObject['endpoint_uri']
    orderShellObject['endpoint_uri'] += '/test'
    testedOrder = await send(orderShellObject, return_query = return_query)
    orderShellObject['endpoint_uri'] = original_endpoint
    return testedOrder

