import json
import config
from flask import Flask, Response, request
from binance_functions import Binance
from binance.client import BinanceAPIException

app = Flask(__name__)

client = Binance(config.API_KEY, config.SECRET_KEY)


def get_request(request_data):
    data_string = str(request_data, "utf-8")
    data = json.loads(data_string)
    passphrase = data["passphrase"]
    symbol = data["symbol"].replace("PERP", "")
    command = data["command"]
    leverage = int(data["leverage"])
    qty = float(data["qty"])
    option = data["option"]
    return symbol, command, qty, leverage, option, passphrase

# API
@app.route('/balances', methods=['GET'])
def balances():
    # if passphrase == config.PASSPHRASE:
    return client.getCoinBalance()

    # else:
    #     return Response("An unauthorized order from TradingView has been blocked. Check your security", 401)



@app.route('/futures', methods=['POST'])
def futures():
    request_data = request.get_data()
    symbol, command, qty, leverage, option, passphrase = get_request(
        request_data)
    if passphrase == config.PASSPHRASE:
        if client.check_position(symbol=symbol) == False:
            if command == 'buy':
                try:
                    client.change_leverage(symbol=symbol, leverage=leverage)
                    client.BUY(symbol=symbol, qty=qty)
                    return Response(f"[BUY : {symbol}] [QTY : {qty}]", 200)
                except BinanceAPIException as e:
                    return Response(f"[Exception : {e}]", 500)

            elif command == 'sell':
                try:
                    client.change_leverage(symbol=symbol, leverage=leverage)
                    client.SELL(symbol=symbol, qty=qty)
                    return Response(f"[SELL : {symbol}] [QTY : {qty}]", 200)
                except BinanceAPIException as e:
                    return Response(f"[Exception : {e}]", 500)
        else:
            position = client.get_position(symbol=symbol)
            if float(position["positionAmt"]) > 0.0:
                side = 'buy'
            else:
                side = 'sell'

            if command == side:
                return Response(f"[Exception : Duplicate]", 500)
            else:
                client.close_position(symbol=symbol)
                return Response(f"[Close : {symbol}]", 200)
    else:
        return Response("An unauthorized order from TradingView has been blocked. Check your security", 401)


@app.route('/scalper', methods=['POST'])
def scalper():
    request_data = request.get_data()
    symbol, command, qty, leverage, option, passphrase = get_request(
        request_data)
    if passphrase == config.PASSPHRASE:
        if client.check_position(symbol=symbol) == False:
            if command == 'buy':
                try:
                    client.change_leverage(symbol=symbol, leverage=leverage)
                    client.BUY(symbol=symbol, qty=qty)
                    return Response(f"[BUY : {symbol}] [QTY : {qty}]", 200)
                except BinanceAPIException as e:
                    return Response(f"[Exception : {e}]", 500)

            elif command == 'sell':
                try:
                    client.change_leverage(symbol=symbol, leverage=leverage)
                    client.SELL(symbol=symbol, qty=qty)
                    return Response(f"[SELL : {symbol}] [QTY : {qty}]", 200)
                except BinanceAPIException as e:
                    return Response(f"[Exception : {e}]", 500)
        else:
            position = client.get_position(symbol=symbol)
            if float(position["positionAmt"]) > 0.0:
                side = 'buy'
            else:
                side = 'sell'

            if command == side:
                return Response(f"[Exception : Duplicate]", 500)
            else:
                if option in ["TP", "C"]:
                    client.close_position(symbol=symbol)
                    return Response(f"[Close : {symbol}]", 200)
                elif option == "L":
                    client.change_leverage(symbol=symbol, leverage=leverage)
                    client.BUY(symbol=symbol, qty=qty)
                    return Response(f"[BUY : {symbol}] [QTY : {qty}]", 200)
                elif option == "S":
                    client.change_leverage(symbol=symbol, leverage=leverage)
                    client.SELL(symbol=symbol, qty=qty)
                    return Response(f"[SELL : {symbol}] [QTY : {qty}]", 200)
                else:
                    return Response("ERROR!")
    else:
        return Response("An unauthorized order from TradingView has been blocked. Check your security", 401)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
