# CoinCortex (Public)

![status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![license](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![python](https://img.shields.io/badge/Python-3.11+-yellow?style=flat-square)
![ai](https://img.shields.io/badge/AI-GPT%20Driven-purple?style=flat-square)

AI-Driven Crypto Trading Assistant

CoinCortex is a modular AI trading system designed to analyze market data, generate signals, and execute trades automatically.  
It integrates multiple data layers (Binance, CoinGlass, DOM Collector) and uses GPT-based models for strategic decision-making.

## Table of Contents
- [Features](#features)
- [Stack](#stack)
- [Architecture Overview](#architecture-overview)
- [Modules Overview](#modules-overview)
- [Roadmap](#coincortex-roadmap-full-engineering-edition)
- [Contributing](#contributing)
- [Installation & Setup](#installation--setup)
- [Status](#status)
- [Disclaimer](#disclaimer)

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

## CoinCortex Roadmap Full Engineering Edition

> This roadmap reflects the *actual internal status* of CoinCortex & DOM Collector  
> — including data systems, AI core, execution engine, and case-learning modules.  
> Updated manually to reflect real development progress.

---

### ✅ PHASE 1 — CORE FOUNDATION *(Completed)*

### 🔧 1.1. Repository & Architecture
- [x] Project structure (utils/, cases/, configs/, engines/, data modules)
- [x] Centralized time_utils (UTC, local, parsing)
- [x] Settings manager (JSON + .env)
- [x] Exception-safe startup & logging pipeline
- [x] Clean GitHub structure with README, diagrams, modules overview

### 🧩 1.2. Data Inputs (Initial Integration)
- [x] Binance API (market data: klines, price, positions snapshot)
- [x] CoinGlass API (OI, funding, long/short ratio, pairs metadata)
- [x] Whale listener (Telethon-based)
- [x] News Parser v2 core logic (RSS + Telegram)
- [x] DOM Collector (external but integrated)

### 🧪 1.3. Demo Mode for Public Repo
- [x] `main.py --demo`
- [x] Features → GPT → Evaluator → Telegram simulation
- [x] Sample outputs, ASCII pipeline, consistent formatting

---

### ⚙️ PHASE 2 — DATA & FEATURE ENGINEERING *(Completed / Ongoing)*

### 📊 2.1. Market Features
- [x] RSI (multi-TF)
- [x] MACD (multi-TF)
- [x] EMA7/25/99 (multi-TF)
- [x] Volume analysis (average, delta)
- [x] Kline normalization (feature bundle)
- [x] Liquidation predictor (basic)
- [x] OI delta computation
- [ ] Funding rate historical trend (planned)
- [ ] Volume Profile (planned)

### 🔁 2.2. DOM Collector (Independent Subsystem)
- [x] Live order book snapshots every 5 seconds
- [x] SQLite storage (high compression)
- [x] Shadow Runner orchestration
- [x] Patterns pipeline (batches → features → GPT-analysis)
- [x] Master patterns analyzer
- [x] GPT pattern classification
- [x] Snapshot indexing, batching, chunking
- [ ] DOM → CaseMatcher integration v2 (planned)
- [ ] DOM-based entry validator (planned)

### 🕯 2.3. Candle Emulator
- [x] Candle emulator v1 (engulfings, breakouts, compressions)
- [ ] Candle emulator v2 (multi-TF, anomaly detection)

---

### 🤖 PHASE 3 — AI CORE & STRATEGY ENGINE *(Partially Complete)*

### 🧠 3.1. GPT Integration
- [x] o4-mini integration (replaced GPT-3.5)
- [x] Prompt loader system (LONG/SHORT/Direction/Strategy)
- [x] Strategy prompts (Scalp / Sniper / Swing)
- [x] Dynamic data injection (RSI, EMA, OI, Funding, DOM, news)
- [x] Case-based reasoning blocks
- [ ] Weight system for reasoning (DOM > Liquidations > News)
- [ ] Multi-model ensemble (GPT-5-nano / 5-mini / 5)

### 🧩 3.2. Case System
- [x] Case logger (auto after every trade)
- [x] Unified case format (RSI/EMA/DOM/Funding/OI/Tags)
- [x] CaseMatcher v1 (similarity via indicators + candles)
- [ ] CaseMatcher v2 (embedding + TF conditions)
- [ ] Automated case clustering (KNN / DBSCAN)
- [ ] Reinforcement from win/loss feedback

---

### ⚔️ PHASE 4 — SIGNAL EVALUATOR & RISK FILTERS *(Completed / Evolving)*

### 🛡 4.1. Hard Filters
- [x] Spread guard
- [x] No-active-position guard
- [x] Multi-pair cooldown registry
- [x] No-entry during volatility spikes (basic)

### 🔬 4.2. Signal Evaluator
- [x] Confidence threshold
- [x] Risk/Reward filter
- [x] SL/TP validation
- [x] News sentiment injection
- [ ] DOM-based precheck v2
- [ ] Knife-protection improvements
- [ ] Multi-session context (Asia/EU/US behavior)

---

### 💰 PHASE 5 — EXECUTION & TRADE ENGINE *(Major Milestone Achieved)*

### ⚙️ 5.1. Trade Execution
- [x] Multi-pair trading support
- [x] Entry percent logic (e.g., /entry 60)
- [x] Auto-correction of entry (dynamic margin fallback)
- [x] Full manual/auto modes
- [x] Futures position snapshot & validation

### 📈 5.2. Position Manager
- [x] TP1 (50%) + TP2 (50%)
- [x] Break-even shift after TP1
- [x] TP2 timers (auto market exit)
- [x] SL/TP existence validation
- [x] Manual close detection
- [x] Trailing stop (experimental)
- [ ] Strategy-driven timing logic (auto-adjust intervals)
- [ ] Dynamic SL tightening

---

### 🛰️ PHASE 6 — ORCHESTRATION & SYSTEM LAYER *(Mostly Complete)*

### 📡 6.1. Telegram System
- [x] Real-time signals formatting
- [x] Distinct LONG/SHORT styling
- [x] Error notifications
- [x] Startup/shutdown messages
- [x] GPT-data forwarding (debug mode)

### 📰 6.2. News & Whale Infrastructure
- [x] News parser v2 (Telegram + RSS)
- [x] Tone detection (bullish / bearish / neutral)
- [x] External event watcher concept
- [x] Whale listener (Telethon)
- [ ] News → GPT contextual block v2
- [ ] Whale → GPT anomaly injector
- [ ] Global sentiment weighting

---

### 🌐 PHASE 7 — PRODUCTIZATION & FUTURE VISION *(Planned)*

### 🖥 7.1. UI / Dashboard
- [ ] Web dashboard (React + FastAPI)
- [ ] Live charts (Price + DOM + Indicators)
- [ ] Case visualizer
- [ ] News sentiment heatmap

### 🌍 7.2. Ecosystem Extensions
- [ ] External API for AI trading signals
- [ ] Shared datasets for research
- [ ] DeFi liquidation/MEV scanner
- [ ] Multi-exchange arbitration layer

---

### 🕓 Last Updated: November 2025
### 📌 Next Big Milestone:
**CaseMatcher v2 + DOM integrated reasoning + strategy weights system.**

## Demo Output Example
Below is an example output produced by:

```bash
python main.py --demo
```
This illustrates the entire CoinCortex pipeline:
Data → Indicators → AI Analysis → Signal Evaluation → Telegram-style message.
```
CoinCortex Demo Mode
------------------------------------------------------------

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

== Data Processing Layer ==
Sample features:
{
  "symbol": "BTCUSDT",
  "rsi_5m": 28.7,
  "macd_5m": { "macd": -12.1, "signal": -10.4, "hist": -1.7 },
  "ema_order_5m": [7, 25, 99],
  "volume_5m_avg": 1230000.0,
  "oi_delta_15m": -0.8,
  "funding": 0.0001
}

== GPT Analysis Core ==
{
  "direction": "LONG",
  "confidence": 0.924,
  "reasons": [
    "RSI(5m) oversold zone",
    "EMA order indicates short-term weakness",
    "Rising negative MACD histogram",
    "OI decreasing (risk-off behavior)"
  ]
}

== Signal Evaluator ==
{
  "approved": true,
  "tp": [
    { "target": "TP1", "delta_pct": 0.35 },
    { "target": "TP2", "delta_pct": 0.85 }
  ],
  "sl": { "target": "SL", "delta_pct": -0.45 },
  "rr": 2.67
}

== Telegram Notifier (simulated) ==
📢 CoinCortex — APPROVED ✅
🧭 Direction: LONG
💠 Symbol: BTCUSDT
🔒 Confidence: 92%
🎯 Targets: TP1 0.35%, TP2 0.85%
🛡 SL: -0.45%
⚖️ R/R: 2.67
📌 Reasons: RSI oversold; EMA weakening; MACD recovery; OI drop
```
This output is fully generated offline without API keys —
the demo simulates the full decision-making pipeline of CoinCortex.

## Contributing
Issues and feature requests are welcome.  
Use the templates in `.github/ISSUE_TEMPLATE/` for:

- 🐞 Bug reports  
- 🚀 Feature ideas  
- ❓ Questions / clarifications  

Pull requests are accepted for:
- Documentation improvements  
- Non-sensitive code (demo mode, utilities)  
- Test coverage  

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

## Status
Currently in deep testing & refactoring phase.  
Live signal validation and multi-pair trading are functional.

### 📄 License
This project is licensed under the MIT License — see the `LICENSE` file for details.

## Disclaimer
This public repository is a **read-only showcase** of the system architecture and approach.  
It does **not** contain private trading logic, credentials, or live keys. Use at your own risk.

