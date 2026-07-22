<div align="center">

# Quant Realtime Backtest Framework

**An ambitious attempt to build a global stock trading platform — and what it taught me about the gap between theory and reality.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/status-archived%20%2F%20educational-orange.svg)]()

</div>

---

## What This Was Supposed to Be

As a first-year university student with a background in quantitative reasoning and a deep interest in financial markets, I set out to build a **production-grade, real-time global stock trading platform** from scratch.

The vision was ambitious:

```
┌─────────────────────────────────────────────────────────────┐
│               Global Trading Platform Architecture           │
├─────────────────┬───────────────────┬───────────────────────┤
│   Data Layer    │  Processing Layer │    Strategy Layer     │
│                 │                   │                       │
│ • Market feeds  │ • Real-time clean │ • Alpha generation    │
│   (NYSE, HKEX,  │   & normalization │ • Risk management     │
│   LSE, TSE...)  │ • Tick-to-bar     │ • Portfolio optim.    │
│ • Order books   │ • Feature eng.    │ • Execution engine    │
│ • Corp. events  │ • Anomaly detect  │ • Backtesting         │
│ • Alt. data     │ • Storage (TB/day)│ • Live trading        │
└─────────────────┴───────────────────┴───────────────────────┘
```

The plan was to support **multi-market, multi-asset, real-time backtesting and strategy evaluation** — comparable to what Renaissance Technologies or Two Sigma run internally.

---

## Why It Failed

I hit three walls, fast.

### 1. Data is the actual business

Getting clean, normalized, survivorship-bias-free historical data for even one market (let alone global) costs **tens of thousands of dollars per year**. Refinitiv Tick History, Bloomberg Terminal, Nasdaq TotalView — none of these are student-budget friendly. Free alternatives (Yahoo Finance, Alpha Vantage) are riddled with gaps, errors, and rate limits.

I spent more time cleaning dirty data than building anything useful.

### 2. The infrastructure cost is non-trivial

Processing tick-by-tick data for thousands of instruments across multiple exchanges generates **terabytes per day**. A proper pipeline needs:
- Low-latency message brokers (Kafka)
- Time-series databases (kdb+, InfluxDB, Arctic)
- Distributed compute (Spark or custom C++)
- Co-location or cloud infrastructure with sub-millisecond networking

The engineering complexity alone is a full-time job for a team of senior engineers.

### 3. The knowledge gap between textbooks and production

Every quantitative finance textbook teaches you Sharpe ratios, factor models, and Black-Scholes. None of them prepare you for:
- Survivorship bias in your backtests
- Transaction cost modeling that actually reflects market impact
- Regime changes that invalidate your strategy parameters
- The difference between a backtest that looks great and a strategy that makes money

I learned more from this failure than from any lecture.

---

## What Got Built (Partial Implementation)

The `lob_arena/` module contains a working **Limit Order Book simulator** — the one component I managed to complete before reality set in:

```
lob_arena/
├── core/          # Order book matching engine
├── strategies/    # Basic strategy implementations (MM, momentum)
├── analytics/     # PnL, Sharpe, spread capture metrics
├── data/          # Data ingestion stubs (Binance tick data)
└── viz/           # Plotly-based replay visualization
```

```bash
# The one thing that actually works:
pip install -e .
python -m lob_arena.cli battle --strategies mm,momentum --steps 10000
```

---

## What I Learned

> **The gap between knowing finance and building finance infrastructure is enormous — and most of that gap is filled with money, time, and engineering headcount that a first-year student simply does not have.**

Specific takeaways:

- **Data quality is 80% of the problem.** No model survives contact with real, dirty market data.
- **Backtesting is easier than it looks, and harder than it seems.** Overfitting to history is trivially easy.
- **Start smaller.** A robust single-strategy, single-asset backtester is more valuable than a broken multi-market platform.
- **Institutional quant infrastructure took decades to build.** Trying to replicate it solo in a semester was never realistic.

---

## What Comes Next

This project is archived. The lessons from it directly informed:
- [`GFlowNet-Alpha-Mining`](https://github.com/hongjin-he/GFlowNet-Alpha-Mining) — a more focused, theory-grounded approach to alpha generation
- [`mathmatical-framework-for-world-models-in-quant-finance`](https://github.com/hongjin-he/mathmatical-framework-for-world-models-in-quant-finance) — the mathematical foundations I wish I had before starting this

---

## For Anyone Who Finds This

If you're a student who also tried to build something too big and ran into the same walls — you're not alone. The failure is the education.

Feel free to use the LOB simulator code for your own learning. It actually works.

---

<div align="center">
<sub>Built (and abandoned) by a first-year university student who learned the hard way · HKUST · 2025</sub>
</div>
