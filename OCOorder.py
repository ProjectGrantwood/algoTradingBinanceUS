from utils import to_precision
#import idGenerator as idgen
    
def OCOorder(side = None, price = None, stopPrice = None, stopLimitPrice = None, quantity = None, quoteOrderQuantity = None, base = 'BTC', quote = 'USD', recvWindow = 1000):
    if side == 'SELL' and stopLimitPrice <= stopPrice:
        print('OCO sell orders must have the limit set higher than the stop')
        return None
    else:
        if stopLimitPrice >= stopPrice:
            print('OCO buy orders must have the limit set lower than the stop')
            return None
    reqInfo = basicOCOOrderShell(side, price, stopPrice, stopLimitPrice, base, quote)
    reqInfo['parameters']['limitClientOrderId'] = reqInfo['paramters']['listClientOrderId'] + 'LIMIT'
    reqInfo['parameters']['stopClientOrderId'] = reqInfo['paramters']['listClientOrderId'] + 'STOP'
    reqInfo = generateQuoteOrQuantity(reqInfo, price, quantity, quoteOrderQuantity, 8)
    return reqInfo

def cancelOCOOrder(requestObject):
    reqInfo = requestObject;
    reqInfo['type'] = 'OCO_ORDER_CANCELLATION',
    reqInfo['endpointType'] = 'DELETE'
    reqInfo['parameters']['origClientOrderId'] = reqInfo['parameters']['listClientOrderId']
    reqInfo['parameters']['newClientOrderId'] = reqInfo['parameters']['listClientOrderId'] + 'CANCEL'
    return reqInfo

def cancelOCOOrderbyId(orderId, base='BTC', quote='USD', recvWindow='1000'):
    symbol = base + quote
    return {
        'type': 'ORDER_CANCELLATION',
        'endpointType': 'DELETE',
        'endpoint_uri': '/api/v3/openOCOOrders',
        'security': 'signed',
        'max_recvWindow': 60000,
        'weight': 2,
        'source': 'matching engine',
        'parameters': {
            'symbol': symbol,
            'orderId': orderId,
            'recvWindow': recvWindow
        },
        'pre_request_information': {
            'status': 'SIGN',
            'message': 'Ready for signature'
        }
    }

def basicOCOOrderShell(side, price, stopPrice, stopLimitPrice, base='BTC', quote='USD', recvWindow = 1000):
    symbol = base + quote
    return {
        'type': 'OCO_ORDER',
        'endpointType': 'POST',
        'endpoint_uri': '/api/v3/order/oco',
        'security': 'signed',
        'max_recvWindow': 60000,
        'weight': 1,
        'source': 'matching engine',
        'parameters': {
            'symbol': symbol,
            'side': side,
            'price': price,
            'stopPrice': stopPrice,
            'stopLimitPrice': stopLimitPrice,
            'recvWindow': recvWindow,
            #'listClientOrderId': idgen.idGenerator.__next__()
        },
        'pre_request_information': {
            'status': 'INITIAL',
            'message': 'Order Information not yet populated'
        }
    }
    
def generateQuoteOrQuantity(orderData, price, quoteOrderQuantity, quantity, precision):
    if quoteOrderQuantity != None and quantity == None:
        orderData['parameters']['quantity'] = to_precision(quoteOrderQuantity / price, precision)
        # Don't attach quoteOrderQty to the parameter list, just keep it around for later reference.
        orderData['quoteOrderQty'] = quoteOrderQuantity
    else:
        if quantity != None:
            orderData['parameters']['quoteOrderQty'] = to_precision(price * quantity, precision)
            orderData['parameters']['quantity'] = quantity
        else:
            orderData['pre_request_information']['status'] = 'ERROR'
            orderData['pre_request_information']['message'] = 'Parameter "quoteOrderQuantity" or Parameter "quantity" must be assigned a value'
            print(orderData['pre_request_information'])
            return orderData['pre_request_information']['status']
    return orderData


    
