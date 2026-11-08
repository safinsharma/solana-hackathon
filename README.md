# 🛡️ Solana GenAI Portfolio & Risk Copilot

> An institutional-grade, natural-language AI agent for real-time Solana mainnet wallet auditing, dynamic risk scoring, and statistical time-series anomaly detection. Built for the **Solana Hackathon (AI Track)**.

---

## Project Overview

Navigating on-chain data on Solana can be overwhelming for everyday users and institutional treasuries alike. Raw JSON-RPC responses, high transaction velocities, and complex token mint balances make manual security auditing difficult.

**Solana GenAI Portfolio & Risk Copilot** solves this problem by combining real-time Solana mainnet RPC data, quantitative time-series data science, and state-of-the-art GenAI LLMs (via Groq `openai/gpt-oss-20b`). 

It provides an **autonomous, smarter, and safer on-chain experience**:
1. **Real-Time On-Chain Data Fetching:** Directly queries Solana mainnet nodes for SOL balances, SPL token account inventories, and transaction block logs (up to 500 signatures).
2. **Deterministic & Dynamic Risk Engine:** Evaluates portfolio exposure, liquidity concentration, and transaction frequency to output a transparent **1–100 Risk Score**.
3. **Time-Series Velocity & Anomaly Forecasting:** Uses `pandas` to aggregate transaction timestamps into intraday hourly frequencies, computing moving average baselines to flag bot/DEX surges automatically.
4. **Natural Language AI Copilot:** Synthesizes multi-dimensional data into clear, institutional-grade audit reports.

---

## AI Track Rubric Alignment

This project specifically targets the **Solana Hackathon AI Track** criteria (*Making on-chain activity smarter, safer, or easier*):

- **Smarter:** Transforms raw, unorganized RPC block signatures and token program accounts into actionable statistical trends and moving average baselines.
- **Safer:** Computes dynamic risk levels and flags unexpected transaction velocity spikes before users sign or commit funds.
- **Easier:** Enables natural-language requests (*"Audit my portfolio risk and check for velocity anomalies"*) to deliver clean executive summaries.
- **Real Work by Both AI & Solana:** 
  - **Solana** provides real-time state data (balances, SPL tokens, Unix block timestamps).
  - **AI (Groq)** interprets contextual parameters, evaluates anomalies, and writes human-readable security audits.

---

## Tech Stack

- **Frontend / UI:** [Streamlit](https://streamlit.io/) (with custom CSS dark-theme polish)
- **Language & Data Processing:** Python 3.10+, [Pandas](https://pandas.pydata.org/)
- **LLM / GenAI Inference:** [Groq API](https://groq.com/) (`openai/gpt-oss-20b`)
- **Blockchain Interface:** Solana JSON-RPC HTTP API (`https://api.mainnet-beta.solana.com`)

---

## Getting Started Locally

Follow these 3 simple steps to run the application on your local machine:

### 1. Prerequisites & Installation

Ensure you have Python 3.10 or higher installed. Clone the repository and install required dependencies:

```bash
git clone https://github.com/your-username/solana-genai-copilot.git
cd solana-genai-copilot

pip install streamlit pandas requests openai
```

### 2. Environment Setup

Set your Groq API Key as an environment variable (or enter it directly into the app sidebar):

```bash
# On Linux/macOS
export GROQ_API_KEY="your_groq_api_key_here"

# On Windows (Command Prompt)
set GROQ_API_KEY="your_groq_api_key_here"

# On Windows (PowerShell)
$env:GROQ_API_KEY="your_groq_api_key_here"
```

### 3. Run the App

Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

---

## How It Works

```
                     ┌────────────────────────────────┐
                     │    Solana Mainnet JSON-RPC     │
                     └───────────────┬────────────────┘
                                     │
                 [getBalance, getTokenAccounts, getSignatures]
                                     │
                                     ▼
                     ┌────────────────────────────────┐
                     │   Data Science & Risk Engine   │
                     │  - Pandas Timestamp Resampling │
                     │  - Rolling Average Baselines   │
                     │  - Deterministic Risk Scoring  │
                     └───────────────┬────────────────┘
                                     │
                          [Structured Context JSON]
                                     │
                                     ▼
 ┌──────────────────────┐    ┌────────────────────────────────┐
 │ User Prompt Input    ├--->│    Groq AI Inference Agent     │
 └──────────────────────┘    │     (openai/gpt-oss-20b)       │
                             └───────────────┬────────────────┘
                                             │
                                             ▼
                             ┌────────────────────────────────┐
                             │ Streamlit Interactive Dashboard│
                             │ - Portfolio Metrics            │
                             │ - AI Audit Report Tab          │
                             │ - Moving Average Baseline Chart│
                             │ - Token & Signature Logs       │
                             └────────────────────────────────┘
```

---

## Quick-Test Wallets

Try testing the app with these pre-configured Solana mainnet targets directly inside the sidebar:

* **Active Whale / Foundation:** `9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM`
  - *Demonstrates handling massive balances (9M+ SOL) and thousands of token accounts.*
* **Active Trader Address:** `MJKqp326RZCHnAAbew9MDdui3iCKWco7fsK9sVuZTX2`
  - *Demonstrates active trading logs and moving average trends.*
* **Clean / New Wallet:** `11111111111111111111111111111111`
  - *Demonstrates graceful fallback handling for empty state wallets.*

---

## Hackathon Achievements Summary

- Fully functional Python + Streamlit application.
- Multi-dimensional risk score logic (1–100 scale).
- Live time-series moving average and anomaly spike detection.
- Hybrid LLM + deterministic fallback mechanism for reliable safety reports.
