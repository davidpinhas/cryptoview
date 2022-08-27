import os
from termios import CINTR
from flask import Flask, render_template, request, flash, redirect, jsonify
from binance.client import Client
from binance.enums import *
from flask_healthz import healthz
from flask_healthz import HealthError

api_key = os.environ.get('BINANCE_API')
api_secret = os.environ.get('BINANCE_SECRET')

app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")

def healthcheck():
    print("Health check passed")

def liveness():
    try:
        healthcheck()
    except Exception:
        raise HealthError("Liveness health check failed")

def readiness():
    try:
        healthcheck()
    except Exception:
        raise HealthError("Readiness health check failed")

app.config.update(
    HEALTHZ = {
        "liveness": "app.liveness",
        "readiness": "app.readiness",
    }
)

client = Client(api_key, api_secret)

@app.route('/')
def index():
    title = 'CryptoView'

    account = client.get_account()

    balances = account['balances']
    coins_list = []
    for asset in balances:
        if float(asset['free']) > 0:
            coins_list.append({'asset': asset['asset'], 'free': asset['free']})

    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']

    return render_template('index.html', title=title, my_balances=coins_list, symbols=symbols)

@app.route('/buy', methods=['POST'])
def buy():
    print(request.form)
    try:
        order = client.create_order(
        symbol=request.form['symbol'],
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/invest', methods=['POST'])
def invest():
    print(request.form)
    try:
        order = client.create_order(
        symbol=request.form['symbol'],
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/stopinvest', methods=['POST'])
def stopinvest():
    print(request.form)
    try:
        order = client.create_order(
        symbol=request.form['symbol'],
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=request.form['quantity'])
    except Exception as e:
        flash(e.message, "error")

    return redirect('/')

@app.route('/sell')
def sell():
    return 'sell'

@app.route('/settings')
def settings():
    return 'settings'

@app.route('/btc_history')
def btc_history():
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    
    btc_processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        btc_processed_candlesticks.append(candlestick)
    return jsonify(btc_processed_candlesticks)

@app.route('/eth_history')
def eth_history():
    candlesticks = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    
    eth_processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        eth_processed_candlesticks.append(candlestick)
    return jsonify(eth_processed_candlesticks)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='5001')
    