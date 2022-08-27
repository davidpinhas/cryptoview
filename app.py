import os
from flask import Flask, render_template, request, flash, redirect, jsonify
from binance.client import Client
from binance.enums import *
from flask_healthz import healthz
from flask_healthz import HealthError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.environ.get('BINANCE_API')
api_secret = os.environ.get('BINANCE_SECRET')

app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")

def healthcheck():
    app.logger.info("Health check passed")

def liveness():
    try:
        app.logger.info("Running liveness check")
        healthcheck()
    except Exception:
        app.logger.error("Liveness probe health check has failed!")
        raise HealthError("Liveness health check failed")

def readiness():
    try:
        app.logger.info("Running readiness check")
        healthcheck()
    except Exception:
        app.logger.error("Readiness probe health check has failed!")
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
            app.logger.info(f"The asset {asset} retrival was successful")
    
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    app.logger.info("Request was successfully sent to index page")
    return render_template('index.html', title=title, my_balances=coins_list, symbols=symbols)

@app.route('/buy', methods=['POST'])
def buy():
    app.logger.info(request.form)
    try:
        order = client.create_order(
        symbol=request.form['symbol'],
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=request.form['quantity'])
        app.logger.info(f"Transaction was successful for {request.form['symbol']} {request.form['quantity']}")
    except Exception as e:
        app.logger.error(f"Transaction has failed")
        flash(e.message, "error")

    return redirect('/')

@app.route('/invest', methods=['POST'])
def invest():
    app.logger.info(request.form)
    try:
        order = client.create_order(
        symbol=request.form['symbol'],
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=request.form['quantity'])
        app.logger.info(f"Starting investing process")
    except Exception as e:
        app.logger.error(f"Failed to start investing trigger")
        flash(e.message, "error")

    return redirect('/')

@app.route('/stopinvest', methods=['POST'])
def stopinvest():
    app.logger.info(request.form)
    try:
        order = client.create_order(
        symbol=request.form['symbol'],
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=request.form['quantity'])
        app.logger.info(f"Stopping investing process")
    except Exception as e:
        app.logger.error(f"Failed to stop investing trigger")
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
        app.logger.debug(f"Retriving BTC data for candlestick {candlestick}")

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
        app.logger.debug(f"Retriving ETH data for candlestick {candlestick}")

    return jsonify(eth_processed_candlesticks)

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='5001')
    