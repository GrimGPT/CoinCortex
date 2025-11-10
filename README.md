# CoinCortex (Public)
AI-Driven Crypto Trading Assistant

CoinCortex is a modular AI trading system designed to analyze market data, generate signals, and execute trades automatically.  
It integrates multiple data layers (Binance, CoinGlass, DOM Collector) and uses GPT-based models for strategic decision-making.

## Features
- 🔍 Real-time market analysis (RSI, MACD, EMA, Volume)
- 🤖 Signal evaluation with GPT (o4-mini / GPT-5)
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
3. **GPT Analysis Core** — prompt-driven reasoning (GPT-5-mini / GPT-5), confidence scoring, case-matching
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
