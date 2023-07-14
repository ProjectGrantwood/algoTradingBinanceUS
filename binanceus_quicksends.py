import asyncio
import pandas_ta as ta
from position import Position
import binanceus_hookup as bush
import orderData as oDat
import priceData as pDat
import tradeData as tDat
import userData as uDat
import generalData as gDat
import OCOOrderData as ocoDat
import order
import OCOorder
from binanceus_request import key_access_client
from utils import num_out, to_precision, transpose
from old.rollingDataCollector import RollingDataCollector


# Server Information ###################################################

async def serverTime(inSeconds = False):
    t = await bush.quickSend(gDat.serverTime)
    t = t.json()["serverTime"]
    if inSeconds:
        t = to_precision(t / 1000, 3)
    return t


# Symbol Information ###################################################


async def pair_info(base='BTC', quote='USD'):
    info = await bush.quickSend(gDat.getTradingPairInfo)
    info = info.json()['symbols']
    syminfo = [sym for sym in info if sym["symbol"] == base + quote]
    return syminfo

async def base_info(base='BTC'):
    info = await bush.quickSend(gDat.getTradingPairInfo)
    info = info.json()['symbols']
    syminfo = [sym for sym in info if sym["baseAsset"] == base]
    return syminfo

async def quote_info(quote='BTC'):
    info = await bush.quickSend(gDat.getTradingPairInfo)
    info = info.json()['symbols']
    syminfo = [sym for sym in info if sym["quoteAsset"] == quote]
    return syminfo

async def current_asset_value(base, quote):
    ticker_price = await bush.quickSend(pDat.getTickerPrice, {'base': base, 'quote': quote})
    ticker_price = ticker_price.json()
    value = None
    try:
        value = num_out(ticker_price['price'])
    except KeyError:
        quote_price = 1.0
        base_price = 1.0
        if base != 'USD':
            base_price = await bush.quickSend(pDat.getTickerPrice, {'base': base, 'quote': 'USD'})
            base_price = num_out(base_price.json()['price'])
        if quote != 'USD':
            quote_price = await bush.quickSend(pDat.getTickerPrice, {'base': quote, 'quote': 'USD'})
            quote_price = num_out(quote_price.json()['price'])
        value = base_price / quote_price
    return value

# Account Information ##################################################

async def get_account(recvWindowOverride=30000):
    acct = await bush.quickSend(uDat.getAccount, recvWindowOverride=recvWindowOverride)
    return acct.json()

async def my_asset_quantity(base='BTC', quote='USD', price_data=True, recvWindowOverride=30000):
    acct = await bush.quickSend(uDat.getAccount, recvWindowOverride = recvWindowOverride)

    free_quantity = None
    locked_quantity = None
    balances = acct.json()
    balances = balances['balances']
    for asset in balances:
        if asset['asset'] == base:
            free_quantity = num_out(asset['free'])
            locked_quantity = num_out(asset['locked'])
            asset_data = {'free': free_quantity, 'locked': locked_quantity}
            if base != quote:
                asset_data['value_in'] = quote
            if price_data and base != quote:
                spot_price = await current_asset_value(base, quote)
                asset_data['freeValue'] = spot_price * asset_data['free']
                asset_data['lockedValue'] = spot_price * asset_data['locked']
            return asset_data
    print('Asset Not Found')
    return False


# Bid, Ask, and gap #################################################


async def best_bid(base='BTC', quote='USD'):
    pdj = await bush.quickSend(pDat.getBestOrderBookPrice, {'base': base, 'quote': quote})
    pdj = pdj.json()
    price_data = {'bidPrice': num_out(pdj['bidPrice']), 'bidQuantity': num_out(pdj['bidQty'])}
    return price_data

async def best_ask(base='BTC', quote='USD'):
    pdj = await bush.quickSend(pDat.getBestOrderBookPrice, {'base': base, 'quote': quote})
    pdj = pdj.json()
    price_data = {'askPrice': num_out(pdj['askPrice']), 'askQuantity': num_out(pdj['askQty'])}
    return price_data

async def best_order_book_price(base='BTC', quote='USD'):
    pdj = await bush.quickSend(pDat.getBestOrderBookPrice, {'base': base, 'quote': quote})
    pdj = pdj.json()
    return num_out(pdj)

async def bid_above(price, base='BTC', quote='USD'):
    currentPrice = await best_bid(base, quote)
    currentPrice = currentPrice['bidPrice']
    return currentPrice > price

async def ask_above(price, base='BTC', quote='USD'):
    currentPrice = await best_ask(base, quote)
    currentPrice = currentPrice['askPrice']
    return currentPrice > price

async def bid_above_last_sale(base='BTC', quote='USD'):
    price = await bush.quickSend(pDat.getTickerPrice, {'base': base, 'quote': quote})
    price = price.json()['price']
    is_above = await bid_above(num_out(price))
    return is_above

async def ask_above_last_sale(base='BTC', quote='USD'):
    price = await bush.quickSend(pDat.getTickerPrice, {'base': base, 'quote': quote})
    price = price.json()['price']
    is_above = await ask_above(num_out(price))
    return is_above

async def bids(base='BTC', quote='USD', limit=5):
    ddj = await bush.quickSend(tDat.getDepth, {'base': base, 'quote': quote, 'limit': limit})
    ddj = ddj.json()
    bid_data = [{'bidPrice': num_out(ddj['bids'][i][0]), 'bidQuantity': num_out(ddj['bids'][i][1])} for i in range(limit)]
    return bid_data

async def asks(base='BTC', quote='USD', limit=5):
    ddj = await bush.quickSend(tDat.getDepth, {'base': base, 'quote': quote, 'limit': limit})
    ddj = ddj.json()
    ask_data = [{'askPrice': num_out(ddj['asks'][i][0]), 'askQuantity': num_out(ddj['asks'][i][1])} for i in range(limit)]
    return ask_data

async def order_book(base='BTC', quote='USD', limit=5):
    ddj = await bush.quickSend(tDat.getDepth, {'base': base, 'quote': quote, 'limit': limit})
    ddj = ddj.json()
    bid_data = [{'bidPrice': num_out(ddj['bids'][i][0]), 'bidQuantity': num_out(ddj['bids'][i][1]), 'askPrice': num_out(ddj['asks'][i][0]), 'askQuantity': num_out(ddj['asks'][i][1])} for i in range(limit)]
    return bid_data

async def ask_and_bid_with_gap(base='BTC', quote='USD', precision=2):
    bobp = await best_order_book_price(base, quote)
    bobp['gap'] = to_precision(bobp['askPrice'] - bobp['bidPrice'], precision)
    return bobp

async def check_gap_for_immediate_loss(lossPercent, base='BTC', quote='USD'):
    abwg = await ask_and_bid_with_gap(base, quote)
    ask = abwg['askPrice']
    gap = abwg['gap']
    if ask - gap <= ask - ask * lossPercent:
        print('Gap is too high, losing sale would trigger immediately: ', 'Ask: ', ask, 'Bid', ask - gap, 'Stop Loss Price', ask - ask * lossPercent)
        return True
    return False

# Chart Data ###########################################################

async def recent_klines(interval, limit, base = "BTC", quote = "USD", recvWindowOverride=None):
    k = await bush.quickSend(tDat.getKlines, {'base': base, 'quote': quote, 'interval': interval, 'limit': limit}, recvWindowOverride=recvWindowOverride)
    return num_out(k.json())

def process_klines(klines, type):
    processed_klines = list()
    for k in range(len(klines)):
        open = klines[k][1]
        high = klines[k][2]
        low = klines[k][3]
        close = klines[k][4]
        processed_kline = None
        match type:
            case 'o':
                processed_kline = open
            case 'h':
                processed_kline = high
            case 'l':
                processed_kline = low
            case 'c':
                processed_kline = close
            case 'ohlc4':
                processed_kline = (open + high + low + close) / 4
            case 'hl2':
                processed_kline = (high + low) / 2
            case 'hlc3':
                processed_kline = (high + low + close) / 3
            case 'hlcc4':
                processed_kline = (high + low + close * 2) / 4
            case 'oohlcc6':
                processed_kline = (open * 2 + high + low + close * 2) / 6
            case 'ohhllc6':
                processed_kline = (open + high * 2 + low * 2 + close) / 6
        processed_klines.append(processed_kline)
    processed_klines = ta.Series(processed_klines)
    return processed_klines

# Ordering #############################################################


async def quickSell(quantity, base='BTC', quote='USD', recvWindowOverride = None):
    sale = await bush.quickSend(order.marketSell, {'base': base, 'quote': quote, 'quantity': quantity}, recvWindowOverride=recvWindowOverride)
    return sale

async def quickBuy(quoteOrderQuantity, base='BTC', quote='USD', precision=8, recvWindowOverride = None):
    purchase = await bush.quickSend(order.marketBuy, {'base': base, 'quote': quote, 'quoteOrderQuantity': quoteOrderQuantity, 'precision': precision}, recvWindowOverride = recvWindowOverride)
    return purchase

async def setLimitBuy(price, quoteOrderQuantity, base='BTC', quote='USD', precision=8):
    purchase = await bush.quickSend(order.limitBuy, {'price': price, 'quoteOrderQuantity': quoteOrderQuantity, 'base': base, 'quote': quote, 'precision': precision})
    return purchase

async def setLimitSell(price, quantity, base='BTC', quote='USD', precision=8):
    sale = await bush.quickSend(order.limitSell, {'price': price, 'quantity': quantity, 'base': base, 'quote': quote, 'precision': precision})
    return sale

async def cancelLimit(orderId, base='BTC', quote='USD'):
    cancellation = await bush.quickSend(order.cancelOrderById, {'orderId': orderId, 'base': base, 'quote': quote})
    return cancellation

def get_average_fill_weighted(orderResponse, precision):
    avPrice = 0.0
    number_of_fills = len(orderResponse['fills'])
    if len == 1:
        return num_out(orderResponse['fills']['0']['price'])
    for i in range(number_of_fills):
        orderResponse['fills'][i] = num_out(orderResponse['fills'][i])
        avPrice = avPrice + orderResponse['fills'][i]['price'] * orderResponse['fills'][i]['qty']
    avPrice = avPrice / orderResponse['executedQty']
    return to_precision(avPrice, precision)

async def sell_when_above(trigger_price, current_bid, positionObject, quote='USD'):
    saleResponse = {}
    if current_bid['bidPrice'] >= trigger_price:
        if current_bid['bidQuantity'] >= positionObject.quantity:
            saleResponse = await quickSell(positionObject.quantity, positionObject.asset, quote)
            if saleResponse.status_code == 200:
                return {'success': True, 'complete_fill': True, 'response': saleResponse}
        else:
            saleResponse = await quickSell(current_bid['bidQuantity'], positionObject.asset, quote)
            if saleResponse.status_code == 200:
                return {'success': True, 'complete_fill': False, 'response': saleResponse}
    return {'success': False, 'response': saleResponse}

async def sell_when_below(trigger_price, current_bid, positionObject, quote='USD'):
    saleResponse = {}
    if current_bid['bidPrice'] <= trigger_price:
        saleResponse = await quick_liquidate_asset(positionObject.asset, quote)
        if saleResponse.status_code == 200:
            return {'success': True, 'complete_fill': True, 'response': saleResponse}
        # if current_bid['bidQuantity'] >= positionObject.quantity:
        #     saleResponse = await quickSell(positionObject.quantity, positionObject.asset, quote)
        #     if saleResponse.status_code == 200:
        #         return {'success': True, 'complete_fill': True, 'response': saleResponse}
        # else:
        #     saleResponse = await quickSell(current_bid['bidQuantity'], positionObject.asset, quote)
        #     if saleResponse.status_code == 200:
                # return {'success': True, 'complete_fill': False, 'response': saleResponse}
    return {'success': False, 'response': saleResponse}

async def buy_when_above(trigger_price, current_ask, quantity, base='BTC', quote='USD'):
    saleResponse = {}
    if current_ask['askPrice'] >= trigger_price:
        if current_ask['askQuantity'] >= quantity:
            saleResponse = await quickBuy(quantity, base, quote)
            if saleResponse.status_code == 200:
                return {'success': True, 'complete_fill': True, 'response': saleResponse}
        else:
            saleResponse = await quickBuy(current_ask['askQuantity'], base, quote)
            if saleResponse.status_code == 200:
                return {'success': True, 'complete_fill': False, 'response': saleResponse}
    return {'success': False, 'response': saleResponse}

async def buy_when_below(trigger_price, current_ask, quantity, base='BTC', quote='USD'):
    saleResponse = {}
    if current_ask['askPrice'] < trigger_price:
        if current_ask['askQuantity'] >= quantity:
            saleResponse = await quickBuy(quantity, base, quote)
            if saleResponse.status_code == 200:
                return {'success': True, 'complete_fill': True, 'response': saleResponse}
        else:
            saleResponse = await quickBuy(current_ask['askQuantity'], base, quote)
            if saleResponse.status_code == 200:
                return {'success': True, 'complete_fill': False, 'response': saleResponse}
    return {'success': False, 'response': saleResponse}

async def quick_liquidate_asset(base, quote='USD', recvWindowOverride=30000):
    asset = await my_asset_quantity(base, quote, False, recvWindowOverride = recvWindowOverride)
    if asset['locked'] > 0:
        cancellation = await bush.quickSend(order.cancelOrdersForSymbol, {'base': base, 'quote': quote}, recvWindowOverride=recvWindowOverride)
        if cancellation.status_code == 200:
            asset['free'] = asset['free'] + asset['locked']
    if asset['free'] > 0:
        sale = await quickSell(asset['free'], base, quote, recvWindowOverride=recvWindowOverride)
        return sale
    print('No free assets to liquidate')
    return False

async def market_trailing_stop_slippage(quoteOrderQuantity, lossPercent, trailTriggerPercent = 0.0007, sleep_time=0.75, slippage=2, base='BTC', quote='USD'):
    gap_too_wide = await check_gap_for_immediate_loss(lossPercent, base, quote)
    if gap_too_wide:
        return False
    purchase = await quickBuy(quoteOrderQuantity, base, quote)
    pos = num_out(purchase.json())
    trading_info = await pair_info(base, quote)
    avPrice = get_average_fill_weighted(pos, trading_info[0]['quoteAssetPrecision'])
    pos = Position(base, trading_info[0]['baseAssetPrecision'], pos['orderId'],  pos['executedQty'], avPrice, pos['transactTime'], True)
    bestPrice = pos.purchase_price
    pos.render()
    lossPrice = to_precision(avPrice - avPrice * lossPercent, trading_info[0]['quoteAssetPrecision'])
    print("Stop Loss Price:", lossPrice, "Prawaice will begin incrementing upward at ", )
    order = await trailing_stop(pos, trailTriggerPercent,sleep_time, slippage, trading_info, base, quote)
    print(order['response'].text)
    return order

async def autoMarketLevelTrade(quoteOrderQuantity, lossPercent, trailTriggerPercent = 0.0007, sleep_time=0.75, slippage=2, buyAtPrice=None, base='BTC', quote='USD', recvWindowOverride=None):
    purchase = buy_at_price(quoteOrderQuantity, buyAtPrice, sleep_time, slippage, base, quote, recvWindowOverride=recvWindowOverride) if buyAtPrice != None else quickBuy(quoteOrderQuantity, base, quote, recvWindowOverride=recvWindowOverride)
    purchase = await purchase
    pos = purchase.json()
    pos = num_out(pos)
    print(pos)
    trading_info = await pair_info(base, quote)
    avPrice = get_average_fill_weighted(pos, trading_info[0]['quoteAssetPrecision'])
    pos = Position(base, trading_info[0]['baseAssetPrecision'], pos['orderId'],  pos['executedQty'], avPrice, pos['transactTime'], True)
    pos.render()
    lossPrice = to_precision(avPrice - avPrice * lossPercent, trading_info[0]['quoteAssetPrecision'])
    trailPrice = to_precision(avPrice + avPrice * trailTriggerPercent, trading_info[0]['quoteAssetPrecision'])
    print("Stop Loss Price:", lossPrice, "Price will begin incrementing upward at ", str(trailPrice))
    order = await trailing_stop(pos, lossPrice, trailTriggerPercent, sleep_time, slippage, trading_info, base, quote)
    print(order['response'].text)
    return order

async def buy_at_price(quoteOrderQuantity, buyAtPrice, sleep_time, slippage, base = "BTC", quote="USD", precision=8, recvWindowOverride=None):
    continueQueryingPrice = True
    purchase = None
    print ("Waiting for price " + str(buyAtPrice))
    while continueQueryingPrice == True:
        top_asks= await asks(base, quote, slippage)
        print(top_asks)
        askPrice = top_asks[-1]['askPrice']
        if askPrice <= buyAtPrice:
            purchase = await quickBuy(quoteOrderQuantity, base, quote, precision, recvWindowOverride = recvWindowOverride)
            if purchase.status_code == 200:
                continueQueryingPrice = False
        else:
            await asyncio.sleep(sleep_time)
    return purchase

async def trailing_stop(pos, lossPrice, trailTriggerPercent, sleep_time, slippage, trading_info, base, quote, reference_bids = True ):
    continueQueryingPrice = True
    broke_even = False
    order = None
    bestPrice = pos.purchase_price
    while continueQueryingPrice == True:
        top_bids= await bids(base, quote, slippage)
        bestbid = top_bids[0]
        bestPrice = top_bids[0]['bidPrice']
        if reference_bids == False:
            ticker_price = await current_asset_value(base, quote)
            bestPrice = ticker_price
        lowbid = top_bids[len(top_bids) - 1]['bidPrice']
        if bestPrice - bestPrice * trailTriggerPercent > pos.purchase_price and broke_even == False:
            broke_even = True
            print("Broke Even")
        print(bestPrice)
        if broke_even == True:
            if reference_bids == True and lowbid > bestPrice:
                bestPrice = lowbid
            if lossPrice < bestPrice - bestPrice  * trailTriggerPercent:
                lossPrice = to_precision(bestPrice - bestPrice * trailTriggerPercent, trading_info[0]['quoteAssetPrecision'])
            print("Trailing Loss Price: ", lossPrice)
        order = await sell_when_below(min(lossPrice, lowbid), bestbid, pos)
        if order['success'] == True:
            if order['complete_fill'] == True:
                continueQueryingPrice = False
            elif order['complete_fill'] == False:
                pos.quantity = to_precision(pos.quantity - num_out(order['response'].json()['executedQty']), pos.asset_precision)
                print(order['response'].json())
        await asyncio.sleep(sleep_time)
    return order
