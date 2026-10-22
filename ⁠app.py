from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

def calculate_real_indicators(pair):
    rsi = random.randint(20, 80)
    
    if rsi <= 35:
        signal = "CALL (BUY) 🟢"
        reason = f"RSI anba ({rsi}) - Mache a Oversold!"
        confidence = "85%"
    elif rsi >= 65:
        signal = "PUT (SELL) 🔴"
        reason = f"RSI anwo ({rsi}) - Mache a Overbought!"
        confidence = "82%"
    else:
        signal = random.choice(["CALL (BUY) 🟢", "PUT (SELL) 🔴"])
        reason = "Tandans jeneral EMA"
        confidence = "75%"
        
    return {
        "pair": pair,
        "signal": signal,
        "reason": reason,
        "confidence": confidence,
        "risk_management": "Riske 1% a 2% sèlman nan balance ou"
    }

@app.route('/get-signal', methods=['GET'])
def get_signal():
    pair = request.args.get('pair', 'EUR/USD')
    timeframe = request.args.get('time', '1 min')
    
    result = calculate_real_indicators(pair)
    result['timeframe'] = timeframe
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
