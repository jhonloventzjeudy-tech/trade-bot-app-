from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import math
import requests

app = Flask(__name__)
CORS(app)

# Mete URL sous done ou verifye a nan anviwònman sèvè a.
# Pa mete kle API prive dirèkteman nan kòd la.
MARKET_DATA_URL = os.getenv("MARKET_DATA_URL", "")

SUPPORTED_PAIRS = {
    "EUR/USD": "EUR/USD",
    "EUR/USD (Real)": "EUR/USD",
    "GBP/USD": "GBP/USD",
    "GBP/USD (Real)": "GBP/USD",
    "BTC/USDT": "BTC/USDT",
}

SUPPORTED_TIMEFRAMES = {
    "15 sec": "15sec",
    "1 min": "1min",
    "5 min": "5min",
    "15 min": "15min",
}


def no_trade(reason, status=200):
    return jsonify({
        "signal": "NO TRADE",
        "reason": reason,
        "verified_data": False,
        "automatic_trading": False
    }), status


def valid_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def validate_candles(candles):
    if not isinstance(candles, list) or len(candles) < 30:
        return False

    for candle in candles:
        if not isinstance(candle, dict):
            return False

        for key in ("open", "high", "low", "close"):
            if not valid_number(candle.get(key)):
                return False

        o = candle["open"]
        h = candle["high"]
        low = candle["low"]
        c = candle["close"]

        if min(o, h, low, c) <= 0:
            return False

        if h < max(o, c, low):
            return False

        if low > min(o, c, h):
            return False

    return True


def calculate_rsi(closes, period=14):
    if len(closes) <= period:
        return None

    changes = [
        closes[i] - closes[i - 1]
        for i in range(1, len(closes))
    ]

    gains = [max(change, 0) for change in changes]
    losses = [max(-change, 0) for change in changes]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (
            avg_gain * (period - 1) + gains[i]
        ) / period

        avg_loss = (
            avg_loss * (period - 1) + losses[i]
        ) / period

    if avg_loss == 0:
        return 100 if avg_gain > 0 else 50

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def 
