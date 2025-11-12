# CoinCortex (Public)
AI-Driven Crypto Trading Assistant

CoinCortex is a modular AI trading system designed to analyze market data, generate signals, and execute trades automatically.  
It integrates multiple data layers (Binance, CoinGlass, DOM Collector) and uses GPT-based models for strategic decision-making.

## Features
- 🔍 Real-time market analysis (RSI, MACD, EMA, Volume)
- 🤖 Signal evaluation with GPT (GPT-5-nano / GPT-5-mini / GPT-5)
- 💬 Telegram integration for live trade alerts
- 🧠 Self-learning case system for pattern matching
- 📊 DOM Collector module for market-maker behavior analysis

## Stack
Python · OpenAI API · SQLite · CoinGlass API · Binance API · Telethon

## Architecture Overview
CoinCortex is structured as a layered pipeline that ingests market data, enriches it with derived metrics, applies AI reasoning, and then delivers actionable trading decisions with automated execution and monitoring.

**Layers**
1. **Data Sources** — Binance, CoinGlass, DOM Collector (order book snapshots)
2. **Data Processing Layer** — normalization, indicators (RSI/MACD/EMA/Volumes), OI/Funding aggregation
3. **GPT Analysis Core** — prompt-driven reasoning (GPT-5-nano / GPT-5-mini / GPT-5), confidence scoring, case-matching
4. **Signal Evaluator** — thresholds, risk filters, strategy rules
5. **Notification & Orchestration** — Telegram alerts, status messages
6. **Position Manager & Auto-Trade** — entry sizing, SL/TP logic, partial take-profit, safety checks

## High-Level Data Flow (ASCII)

```
   [ Binance ] [ CoinGlass ] [ DOM Collector ]
      \ | /        \ | /          \ | /
   \ Data Processing Layer (RSI, MACD, EMA, OI, Funding, Volumes)
    ________________________/
                     |
                     v
             GPT Analysis Core
         (GPT-5-mini / GPT-5 logic)
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
```

## Modules Overview

> High-level map of the public CoinCortex architecture. File names are indicative; private logic and keys are not included.

### 1) Data Sources
- **binance_api.py** — market data adapter (prices, klines, positions snapshot)  
  *Input:* REST/WebSocket (Binance) • *Output:* normalized ticks/klines JSON  
- **coinglass_api.py** — analytics adapter (OI, funding, long/short ratio, pairs metadata)  
  *Input:* CoinGlass REST • *Output:* OI/funding deltas, aggregated metrics  
- **dom_collector/** *(external project)* — order book snapshots for MM behaviour  
  *Input:* Order book • *Output:* DOM features (imbalance, spoof/absorption scores)

### 2) Feature & Metrics Layer
- **volume_analyzer.py** — rolling volume/Delta, average volume filters  
  *Input:* klines • *Output:* volume features  
- **liquidation_predictor.py** — simple liquidation-bias features (public subset)  
  *Input:* OI + price move • *Output:* liquidations bias signals  
- **indicators.py** — RSI, MACD, EMA7/25/99 (multi-TF summary)  
  *Input:* klines • *Output:* indicator bundle
- **candle_emulator.py** — synthetic candlestick summary builder for prompt context when chart images are not available.  
  *Input:* raw OHLC klines • *Output:* text summary of recent price action (engulfings, breakouts, compressions)  

### 3) AI Core & Strategy
- **gpt_interface.py** — prompt execution & parsing (o4-mini / GPT-5)  
  *Input:* feature bundle + context • *Output:* direction + confidence (+ notes)  
- **prompts_loader.py** — templates for LONG/SHORT/direction/strategy prompts  
  *Input:* prompt files • *Output:* hydrated prompts  
- **strategy_selector.py** — chooses scenario (scalp / sniper / swing)  
  *Input:* market regime + rules • *Output:* strategy profile

### 4) Signal Evaluator
- **signal_precheck.py** — hard guards (no active position, spread/filter checks)  
  *Input:* features + open positions • *Output:* pass/fail  
- **case_matcher.py** — compares with past cases (pattern similarity)  
  *Input:* recent case DB • *Output:* nearest cases summary  
- **risk_filters.py** — thresholds (min confidence, RR, session/vol filters)  
  *Input:* analysis + strategy • *Output:* approved/review
- **case_matcher.py** — compares new signals with historical cases using similarity search (RSI, EMA, DOM, volume patterns).  
  *Input:* current feature snapshot • *Output:* closest historical matches with outcome labels  

### 5) Execution & Risk Management
- **trading_engine.py** — single entrypoint for orders (demo only in public)  
  *Input:* approved signal • *Output:* order params (size, price type)  
- **position_manager.py** — TP1/TP2, SL, BE, timers, sanity checks  
  *Input:* live position snapshot • *Output:* adjustments + notifications  
- **trade_executor.py** — routes to exchange (disabled in public repo)  
  *Input:* order params • *Output:* exchange response (mocked in demo)

### 6) Orchestration & Messaging
- **telegram_controller.py** — rendering of human-readable alerts  
  *Input:* signal/position state • *Output:* text payload for Telegram  
- **news_parser_v2.py** *(planned public summary)* — RSS/Telegram parsing + tone  
  *Input:* feeds • *Output:* bullish/bearish/neutral summary  
- **telethon_whale_listener.py** — Telegram-based whale transaction listener built on Telethon API.  
  *Input:* on-chain whale alerts (> 10 M USD transfers or exchange movements) • *Output:* parsed event JSON with timestamp and direction (“deposit”, “withdrawal”, “accumulation”) for AI context blocks.  

### 7) System & Utilities
- **settings_manager.py** — project-wide config (JSON/.env)  
- **time_utils.py** — UTC/Local time helpers, formatted timestamps  
- **case_logger.py** — writes finished trades as compact cases (JSON)

> **Demo status:** The public repo contains a self-contained demo (`main.py --demo`) that simulates the pipeline without live keys/exchange access. Private trading logic remains in closed source.

## Status
Currently in deep testing & refactoring phase.  
Live signal validation and multi-pair trading are functional.

## Disclaimer
This public repository is a **read-only showcase** of the system architecture and approach.  
It does **not** contain private trading logic, credentials, or live keys. Use at your own risk.

## Installation & Setup
> Demo mode runs locally without API keys or external services.  
> It simulates the CoinCortex pipeline and prints a sample trade signal.

### Prerequisites
- Python 3.11+ (Windows/macOS/Linux)
- Git (optional, for cloning)

### 1) Clone (or download)

```bash
git clone https://github.com/GrimGPT/CoinCortex.git
cd CoinCortex
```

### 2) (Optional) Create a virtual environment

```Windows (PowerShell)
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

```macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Run the demo

```
python main.py --demo
```
