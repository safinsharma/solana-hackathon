import os
import json
import pandas as pd
from openai import OpenAI
from solana_service import get_sol_balance, get_spl_tokens, get_recent_transactions
import streamlit as st

api_key = ""
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    elif "OPENAI_API_KEY" in st.secrets:
        api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.environ.get("GROQ_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

def calculate_risk_score(sol_balance: float, tx_count: int, token_count: int) -> dict:
    score = 10
    if sol_balance > 1000000:
        score += 25
    elif sol_balance > 1000:
        score += 15
    elif sol_balance > 100:
        score += 10
        
    if tx_count >= 100:
        score += 35
    elif tx_count >= 10:
        score += 20
        
    if token_count > 100:
        score += 25
        
    score = min(score, 100)
    
    if score >= 75:
        level = "High Risk / High Activity"
    elif score >= 45:
        level = "Moderate Risk / Active Trader"
    else:
        level = "Low Risk / Conservative Holding"
        
    return {"score": score, "level": level}

def analyze_time_series_trend(recent_txs):
    """Calculates rolling average and trend status from transaction timestamps."""
    df_tx = pd.DataFrame(recent_txs)
    df_valid = df_tx[df_tx["timestamp"] != "N/A"].copy()
    
    if df_valid.empty:
        return {"trend_status": "Insufficient Data", "spike_detected": False}
        
    df_valid["datetime"] = pd.to_datetime(df_valid["timestamp"])
    df_valid = df_valid.sort_values("datetime")
    df_valid.set_index("datetime", inplace=True)
    
    # Use lowercase 'h' for Pandas 2.0+ compatibility
    hourly_counts = df_valid.resample("h").size()
    rolling_avg = hourly_counts.rolling(window=3, min_periods=1).mean()
    
    recent_momentum = hourly_counts.iloc[-1] if not hourly_counts.empty else 0
    baseline = rolling_avg.iloc[-1] if not rolling_avg.empty else 0
    
    spike_detected = recent_momentum > (1.5 * baseline) if baseline > 0 else False
    trend_status = "Accelerating / High Activity Spike" if spike_detected else "Stable Activity Baseline"
    
    return {
        "hourly_counts": hourly_counts,
        "rolling_avg": rolling_avg,
        "trend_status": trend_status,
        "spike_detected": spike_detected
    }

def run_copilot(user_prompt: str, wallet_address: str):
    current_key = os.environ.get("GROQ_API_KEY", "")
    if current_key:
        client.api_key = current_key

    # Fetch onchain data directly
    sol_balance = get_sol_balance(wallet_address)
    tokens = get_spl_tokens(wallet_address)
    recent_txs = get_recent_transactions(wallet_address, limit=500)
    
    # Run time-series analytics
    ts_analysis = analyze_time_series_trend(recent_txs)

    # Ensure boolean is explicitly standard Python bool to prevent JSON serialization errors
    spike_val = bool(ts_analysis.get("spike_detected", False))

    system_instruction = (
        "You are an expert AI blockchain financial analyst. "
        "Analyze the user's wallet holdings, risk factors, and time-series transaction trends. "
        "Incorporate statistical velocity shifts or activity spikes into your assessment. "
        "Keep your output professional, well-structured, and under 300 words."
    )

    context_data = {
        "wallet": wallet_address,
        "sol_balance": sol_balance,
        "tokens_count": len(tokens),
        "recent_txs_retrieved": len(recent_txs),
        "time_series_trend": ts_analysis.get("trend_status", "Stable"),
        "anomaly_spike_detected": spike_val
    }

    messages = [
        {"role": "system", "content": system_instruction},
        {
            "role": "user",
            "content": f"User Request: {user_prompt}\n\nWallet Analytics Data:\n{json.dumps(context_data, indent=2)}"
        }
    ]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            max_tokens=1000
        )
        
        final_content = response.choices[0].message.content
        
        if not final_content or "can't help" in final_content.lower() or "sorry" in final_content.lower():
            risk = calculate_risk_score(sol_balance, len(recent_txs), len(tokens))
            final_content = (
                f"### Portfolio & Time-Series Executive Summary\n"
                f"**Target Wallet:** `{wallet_address}`\n\n"
                f"* **Risk Score:** `{risk['score']}/100` ({risk['level']})\n"
                f"* **Native SOL Balance:** `{sol_balance:,.4f} SOL`\n"
                f"* **Activity Trend:** `{ts_analysis.get('trend_status', 'Stable')}`\n"
                f"* **Anomaly Spike Detected:** `{'Yes' if spike_val else 'Normal'}`\n"
            )
            
        return final_content, sol_balance, tokens, recent_txs, ts_analysis

    except Exception as e:
        return f"Error running copilot: {str(e)}", sol_balance, tokens, recent_txs, {}
