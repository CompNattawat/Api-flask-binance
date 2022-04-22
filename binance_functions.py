from binance.client import Client, BinanceAPIException


class Binance(object):
    def __init__(self, api_key, secret_key):
        self.client = Client(api_key, secret_key)

    def get_position(self, symbol):
        positions = self.client.futures_position_information()
        for position in positions:
            if position['symbol'] == symbol:
                break
        return (position)

    def check_position(self, symbol):
        position = self.get_position(symbol)

        in_position = False

        if float(position["positionAmt"]) != 0.0:
            in_position = True

        return in_position

    def close_position(self, symbol):
        position = self.get_position(symbol)
        qty = float(position["positionAmt"])

        side = "BUY"
        if qty > 0.0:
            side = "SELL"

        if qty < 0.0:
            qty = qty * -1

        qty = str(qty)

        self.excute(symbol, type="MARKET", side=side,
                    quantity=qty)

    def excute(self, symbol, type, side, positionSide="BOTH", quantity=0):
        self.client.futures_create_order(
            symbol=symbol, type=type, side=side, positionSide=positionSide, quantity=quantity)

    def excute_takeprofit(self, symbol, side, stopPrice=0):
        self.client.futures_create_order(symbol=symbol, type="TAKE_PROFIT_MARKET",
                                         side=side, closePosition="True", stopPrice=stopPrice, workingType="MARK_PRICE")

    def excute_stoploss(self, symbol, side, stopPrice=0):
        self.client.futures_create_order(symbol=symbol, type="STOP_MARKET",
                                         side=side, closePosition="True", stopPrice=stopPrice, workingType="MARK_PRICE")

    def excute_trailing_stop(self, symbol, side, activationPrice, callbackRate=0, quantity=0):
        self.client.futures_create_order(symbol=symbol, type="TRAILING_STOP_MARKET", side=side,
                                         activationPrice=activationPrice, callbackRate=callbackRate, quantity=quantity)

    def market_precision(self, symbol):
        market_data = self.client.futures_exchange_info()
        qtyprecision = 3
        for market in market_data['symbols']:
            if market['symbol'] == symbol:
                qtyprecision = market['quantityPrecision']
                break
        return qtyprecision

    def round_to_precision(self, x, precision):
        new_qty = "{:0.0{}f}".format(x, precision)
        return float(new_qty)

    def change_leverage(self, symbol, leverage):
        self.client.futures_change_leverage(symbol=symbol, leverage=leverage)

    def BUY(self, symbol, qty):
        qtyprecision = self.market_precision(symbol)
        p_qty = self.round_to_precision(x=qty, precision=qtyprecision)
        self.excute(symbol, type="MARKET", side="BUY", quantity=p_qty)

    def SELL(self, symbol, qty):
        qtyprecision = self.market_precision(symbol)
        p_qty = self.round_to_precision(x=qty, precision=qtyprecision)
        self.excute(symbol, type="MARKET", side="SELL", quantity=p_qty)

    def getCoinBalance(self):
        balance = self.client.get_account()
        return balance
