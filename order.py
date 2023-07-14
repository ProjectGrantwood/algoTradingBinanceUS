from utils import to_precision
# import idGenerator as idgen


# def quickBuyAndSell(valueQuote, base='BTC', quote='USD', recvWindow=1000):
#     buyOrder = marketBuy(valueQuote, base, quote)
    

def marketBuy(quoteOrderQuantity=None, quantity=None, base='BTC', quote='USD', precision = 8, recvWindow=1000):
    reqInfo = basicOrderShell('BUY', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'MARKET'
    reqInfo['precision'] = precision
    if quoteOrderQuantity == None:
        if quantity == None:
            reqInfo['pre_request_information']['status'] = 'ERROR'
            reqInfo['pre_request_information']['message'] = 'Parameter "quoteOrderQuantity" or Parameter "quantity" must be assigned a value'
            print(reqInfo['pre_request_information'])
            return reqInfo['pre_request_information']['status']
        else:
            reqInfo['parameters']['quantity'] = quantity
    else:
        reqInfo['parameters']['quoteOrderQty'] = quoteOrderQuantity
    reqInfo['pre_request_information']['status'] = 'SIGN'
    reqInfo['pre_request_information']['message'] = 'Order ready for signature'
    return reqInfo

def marketSell(quantity = None, quoteOrderQuantity = None, base='BTC', quote='USD', precision=8, recvWindow=1000):
    reqInfo = basicOrderShell('SELL', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'MARKET'
    reqInfo['precision'] = precision
    if quantity == None:
        if quoteOrderQuantity == None:
            reqInfo['pre_request_information']['status'] = 'ERROR'
            reqInfo['pre_request_information']['message'] = 'Parameter "quoteOrderQuantity" or Parameter "quantity" must be assigned a value'
            print(reqInfo['pre_request_information'])
            return reqInfo['pre_request_information']['status']
        else:
            reqInfo['parameters']['quoteOrderQty'] = quoteOrderQuantity
    else:
        reqInfo['parameters']['quantity'] = quantity
    reqInfo['pre_request_information']['status'] = 'SIGN'
    reqInfo['pre_request_information']['message'] = 'Order ready for signature'
    return reqInfo

def stopLoss(price = None, stopPrice = None, quoteOrderQuantity = None, quantity = None, timeInForce='GTC', base='BTC', quote='USD', precision=8, recvWindow = 1000):
    reqInfo = basicOrderShell('SELL', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'STOP_LOSS'
    reqInfo['parameters']['stopPrice'] = stopPrice
    reqInfo = generateQuoteOrQuantity(reqInfo, price, quoteOrderQuantity, quantity, precision)
    return reqInfo

def takeProfit(price = None, stopPrice = None, quoteOrderQuantity = None, quantity = None, timeInForce='GTC', base='BTC', quote='USD', precision=8, recvWindow = 1000):
    reqInfo = basicOrderShell('SELL', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'TAKE_PROFIT'
    reqInfo['parameters']['stopPrice'] = stopPrice
    reqInfo = generateQuoteOrQuantity(reqInfo, price, quoteOrderQuantity, quantity, precision)
    return reqInfo


def limitBuy(price = None, quoteOrderQuantity=None, quantity=None, timeInForce='GTC', base='BTC', quote='USD', precision = 8, recvWindow=1000):
    reqInfo = basicOrderShell('BUY', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'LIMIT'
    reqInfo = generateQuoteOrQuantity(reqInfo, price, quoteOrderQuantity, quantity, precision)
    reqInfo['parameters']['price'] = price
    reqInfo['parameters']['timeInForce'] = timeInForce
    reqInfo['pre_request_information']['status'] = 'SIGN'
    reqInfo['pre_request_information']['message'] = 'Order ready for signature'
    return reqInfo

def limitSell(price=None, quoteOrderQuantity=None, quantity=None, timeInForce='GTC', base='BTC', quote='USD', precision = 8, recvWindow=1000):
    reqInfo = basicOrderShell('SELL', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'LIMIT'
    reqInfo = generateQuoteOrQuantity(reqInfo, price, quoteOrderQuantity, quantity, precision)
    reqInfo['parameters']['price'] = price
    reqInfo['parameters']['timeInForce'] = timeInForce
    reqInfo['pre_request_information']['status'] = 'SIGN'
    reqInfo['pre_request_information']['message'] = 'Order ready for signature'
    return reqInfo

def stopLossLimit(price = None, stopPrice = None, quoteOrderQuantity = None, quantity = None, timeInForce='GTC', base='BTC', quote='USD', precision=8, recvWindow = 1000):
    reqInfo = basicOrderShell('SELL', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'STOP_LOSS_LIMIT'
    reqInfo['parameters']['stopPrice'] = stopPrice
    reqInfo['parameters']['price'] = price
    reqInfo['parameters']['timeInForce'] = timeInForce
    reqInfo = generateQuoteOrQuantity(reqInfo, price, quoteOrderQuantity, quantity, precision)
    return reqInfo

def takeProfitLimit(price = None, stopPrice = None, quoteOrderQuantity = None, quantity = None, timeInForce='GTC', base='BTC', quote='USD', precision=8, recvWindow = 1000):
    reqInfo = basicOrderShell('SELL', base, quote, recvWindow)
    reqInfo['parameters']['type'] = 'TAKE_PROFIT_LIMIT'
    reqInfo['parameters']['stopPrice'] = stopPrice
    reqInfo['parameters']['price'] = price
    reqInfo['parameters']['timeInForce'] = timeInForce
    reqInfo = generateQuoteOrQuantity(reqInfo, price, quoteOrderQuantity, quantity, precision)
    return reqInfo

def cancelOrder(requestObject):
    reqInfo = requestObject
    reqInfo['endpointType'] = 'DELETE'
    reqInfo['parameters']['origClientOrderId'] = reqInfo['parameters']['newClientOrderId']
    reqInfo['parameters']['newClientOrderId'] = reqInfo['parameters']['newClientOrderId'] + 'CANCEL'
    return reqInfo

def cancelOrderById(orderId, base='BTC', quote='USD', recvWindow = 1000):
    symbol = base + quote
    return {
        'type': 'ORDER_CANCELLATION',
        'endpointType': 'DELETE',
        'endpoint_uri': '/api/v3/openOrders',
        'security': 'signed',
        'max_recvWindow': 60000,
        'weight': 1,
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

def cancelOrdersForSymbol(base='BTC', quote='USD', recvWindow=1000):
    symbol = base + quote
    return {
        'type': 'ORDER_CANCELLATION',
        'endpointType': 'DELETE',
        'endpoint_uri': '/api/v3/openOrders',
        'security': 'signed',
        'max_recvWindow': 60000,
        'weight': 1,
        'source': 'matching engine',
        'parameters': {
            'symbol': symbol,
            'recvWindow': recvWindow
        },
        'pre_request_information': {
            'status': 'SIGN',
            'message': 'Ready for signature'
        }
    }
    
    
    
    

def basicOrderShell(side, base='BTC', quote='USD', recvWindow=1000):
    symbol = base + quote
    return {
        'type': 'ORDER',
        'endpointType': 'POST',
        'endpoint_uri': '/api/v3/order',
        'security': 'signed',
        'max_recvWindow': 60000,
        'weight': 1,
        'source': 'matching engine',
        'parameters': {
            'symbol': symbol,
            'side': side,
            'recvWindow': recvWindow,
        # Is a client-generated order ID truly needed?
        #    'newClientOrderId': idgen.idGenerator.__next__()
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
        if quantity != None and orderData['parameters']['side'] != 'SELL':
            orderData['parameters']['quoteOrderQty'] = to_precision(price * quantity, precision)
            orderData['parameters']['quantity'] = quantity
        else:
            orderData['pre_request_information']['status'] = 'ERROR'
            orderData['pre_request_information']['message'] = 'Parameter "quoteOrderQuantity" or Parameter "quantity" must be assigned a value'
            print(orderData['pre_request_information'])
            return orderData['pre_request_information']['status']
    return orderData


    
