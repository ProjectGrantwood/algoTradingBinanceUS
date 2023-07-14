from utils import to_precision

class Position:
    
    def __init__(self, asset, asset_precision, orderId, quantity, purchase_price, timestamp, open):
        self.asset = asset
        self.asset_precision = asset_precision
        self.orderId = orderId
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.purchase_usd_value = to_precision(purchase_price * quantity, 2)
        self.timestamp = timestamp
        self.open = open
    
    def render(self):
        self.display_string = 'Order ' + str(self.orderId) + ': ' + str(self.quantity) + ' ' + self.asset + ' purchased at '+ str(self.purchase_price) + ' USD at a total value of $' + str(self.purchase_usd_value)
        print(self.display_string)