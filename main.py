```
python

import argparse
import json
import random
import sys
import time
from datetime import datetime

ASCII_FLOW = r"""
[ Binance ]   [ CoinGlass ]   [ DOM Collector ]
        \           |                /
         \          |               /
          \         |              /
     Data Processing Layer (RSI, MACD, EMA, OI, Funding, Volumes)
     ________________________/
                 |
                 v
         GPT Analysis Core
        (o4-mini / GPT-5 logic)
                 |
                 v
           Signal Evaluator
          (filters, thresholds)
                 |
                 v
          Telegram Notifier
    (alerts, status, error reports)
                 |
                 v
   Position Manager & Auto-Trade Engine
 (entry %, SL/TP, partials, break-even, timers)
"""

def print_step(title: str):
    print(f"\n== {title} ==")

def simulate_data_layer():
    time.sleep(0.2)
    return {
        "symbol": "BTCUSDT",
        "rsi_5m": 28.7,
        "macd_5m": {"macd": -12.1, "signal": -10.4, "hist": -1.7},
        "ema_order_5m": [7, 25, 99],
        "volume_5m_avg": 1.23e6,
        "oi_delta_15m": -0.8,
        "funding": 0.0001,
    }

def simulate_gpt_analysis(features: dict):
    time.sleep(0.2)
    base_conf = random.uniform(0.82, 0.97)
    direction = "LONG" if features["rsi_5m"] < 30 else "SHORT"
    reasons = [
        "RSI(5m) oversold zone",
        "EMA order indicates short-term weakness",
        "Rising negative MACD histogram",
        "OI decreasing (risk-off behavior)"
    ]
    return {
        "direction": direction,
        "confidence": round(base_conf, 3),
        "reasons": reasons[: random.randint(2, len(reasons))]
    }

def simulate_signal_evaluator(analysis: dict):
    time.sleep(0.2)
    tp1 = {"target": "TP1", "delta_pct": 0.35}
    tp2 = {"target": "TP2", "delta_pct": 0.85}
    sl  = {"target": "SL",  "delta_pct": -0.45}
    rr  = round((tp1["delta_pct"] + tp2["delta_pct"]) / abs(sl["delta_pct"]), 2)
    return {
        "approved": analysis["confidence"] >= 0.9,
        "tp": [tp1, tp2],
        "sl": sl,
        "rr": rr,
    }

def format_telegram_signal(symbol: str, analysis: dict, eval_res: dict):
    status = "APPROVED ✅" if eval_res["approved"] else "REVIEW ⚠️"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"📢 CoinCortex — {status}",
        f"⏱ {now}",
        f"💠 Symbol: {symbol}",
        f"🧭 Direction: {analysis['direction']}",
        f"🔒 Confidence: {int(analysis['confidence']*100)}%",
        f"🎯 Targets: " + ", ".join([f"{t['target']} {t['delta_pct']}%" for t in eval_res["tp"]]),
        f"🛡 SL: {eval_res['sl']['delta_pct']}%",
        f"⚖️ R/R: {eval_res['rr']}",
        "📌 Reasons: " + "; ".join(analysis["reasons"]),
    ]
    return "\n".join(lines)

def run_demo():
    print("\nCoinCortex Demo Mode")
    print("-" * 60)
    print(ASCII_FLOW)

    print_step("Data Processing Layer")
    features = simulate_data_layer()
    print("Sample features:")
    print(json.dumps(features, indent=2))

    print_step("GPT Analysis Core")
    analysis = simulate_gpt_analysis(features)
    print(json.dumps(analysis, indent=2))

    print_step("Signal Evaluator")
    eval_res = simulate_signal_evaluator(analysis)
    print(json.dumps(eval_res, indent=2))

    print_step("Telegram Notifier (simulated)")
    msg = format_telegram_signal(features["symbol"], analysis, eval_res)
    print(msg)

def main(argv=None):
    parser = argparse.ArgumentParser(description="CoinCortex public demo")
    parser.add_argument("--demo", action="store_true", help="run demo pipeline")
    args = parser.parse_args(argv)

    if args.demo:
        run_demo()
    else:
        print("Use --demo to run the local simulation.\nExample:\n  python main.py --demo")
        sys.exit(0)

if __name__ == "__main__":
    main()
```
