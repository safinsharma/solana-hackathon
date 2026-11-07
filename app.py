import streamlit as st
import os
import pandas as pd
from copilot_agent import run_copilot, calculate_risk_score, analyze_time_series_trend

# Page Configuration
st.set_page_config(
    page_title="Solana GenAI Portfolio & Risk Copilot",
    page_icon="🛡️",
    layout="wide"
)

# --- CUSTOM CSS STYLING ---
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .risk-badge-low { background-color: #1b4332; color: #52b788; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .risk-badge-mod { background-color: #533f04; color: #ffb703; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .risk-badge-high { background-color: #5c1815; color: #e76f51; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# App Header
st.title("🛡️ Solana GenAI Portfolio & Risk Copilot")
st.markdown("Your autonomous onchain assistant for real-time wallet auditing, dynamic risk scoring, and **time-series anomaly detection**.")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    groq_key = st.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
    if groq_key:
        os.environ["GROQ_API_KEY"] = groq_key
        
    st.markdown("---")
    st.markdown("### 💡 Quick-Test Wallets")
    if st.button("🐋 Active Whale / Foundation"):
        st.session_state["wallet_input"] = "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
    if st.button("⚡ Active Trader Address"):
        st.session_state["wallet_input"] = "MJKqp326RZCHnAAbew9MDdui3iCKWco7fsK9sVuZTX2"
    if st.button("✨ Clean / Empty Wallet"):
        st.session_state["wallet_input"] = "11111111111111111111111111111111"

# Main Input Controls
default_wallet = st.session_state.get("wallet_input", "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM")
wallet_address = st.text_input("Solana Wallet Address:", value=default_wallet)

user_query = st.text_input(
    "Ask your Copilot anything:", 
    value="Perform a risk audit, check token concentration, and analyze time-series velocity anomalies."
)

col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    analyze_clicked = st.button("Run Audit 🚀", type="primary", use_container_width=True)

if analyze_clicked:
    if not os.environ.get("GROQ_API_KEY"):
        st.error("⚠️ Please enter your Groq API Key in the sidebar first!")
    elif not wallet_address.strip():
        st.error("⚠️ Please enter a valid Solana wallet address.")
    else:
        with st.spinner("🤖 Copilot is analyzing blockchain time-series data, computing rolling baselines, and scoring risk..."):
            try:
                response_text, sol_balance, tokens, recent_txs, ts_analysis = run_copilot(user_query, wallet_address.strip())
                risk = calculate_risk_score(sol_balance, len(recent_txs), len(tokens))
                
                # --- Metrics Row ---
                st.markdown("---")
                st.subheader("📊 Portfolio At-a-Glance")
                
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric(label="Native Balance", value=f"{sol_balance:,.2f} SOL")
                with m2:
                    st.metric(label="SPL Token Accounts", value=len(tokens))
                with m3:
                    st.metric(label="Signatures Tracked", value=len(recent_txs))
                with m4:
                    st.metric(label="Computed Risk Score", value=f"{risk['score']} / 100")
                
                risk_label_html = f"<span class='risk-badge-low'>{risk['level']}</span>"
                if "High" in risk['level']:
                    risk_label_html = f"<span class='risk-badge-high'>{risk['level']}</span>"
                elif "Moderate" in risk['level']:
                    risk_label_html = f"<span class='risk-badge-mod'>{risk['level']}</span>"
                    
                st.markdown(f"**Risk Classification:** {risk_label_html}", unsafe_allow_html=True)
                st.markdown("---")
                
                # --- Tabs ---
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🤖 AI Intelligence Report", 
                    "📈 Velocity & Trend Forecasting", 
                    "🪙 SPL Token Holdings", 
                    "📜 Recent Transactions"
                ])
                
                with tab1:
                    st.markdown("### Copilot Audit Report")
                    st.markdown(response_text)
                    
                with tab2:
                    st.markdown("### Transaction Velocity Trend & Moving Average Baseline")
                    if ts_analysis and "hourly_counts" in ts_analysis and not ts_analysis["hourly_counts"].empty:
                        col_t1, col_t2 = st.columns(2)
                        with col_t1:
                            st.metric(label="Detected Trend Status", value=ts_analysis["trend_status"])
                        with col_t2:
                            spike_status = "Yes ⚠️ (Potential Bot/DEX Spike)" if ts_analysis["spike_detected"] else "Normal Baseline ✅"
                            st.metric(label="Anomaly Status", value=spike_status)
                            
                        st.markdown("#### Hourly Activity vs. Rolling Average Baseline")
                        chart_df = pd.DataFrame({
                            "Hourly Volume": ts_analysis["hourly_counts"],
                            "Rolling Baseline": ts_analysis["rolling_avg"]
                        })
                        st.line_chart(chart_df)
                        
                        st.write("#### Raw Time-Series Log")
                        df_tx = pd.DataFrame(recent_txs)
                        st.dataframe(df_tx[df_tx["timestamp"] != "N/A"][["timestamp", "signature"]], use_container_width=True)
                    else:
                        st.info("Insufficient timestamp data available for time-series forecasting.")
                        
                with tab3:
                    st.markdown("### Active Token Mints & Balances")
                    if tokens:
                        st.dataframe(tokens, use_container_width=True)
                    else:
                        st.info("No active non-zero SPL token balances found for this address.")
                        
                with tab4:
                    st.markdown("### Onchain Transaction Signatures")
                    if recent_txs:
                        for idx, tx in enumerate(recent_txs):
                            sig = tx.get("signature", "N/A")
                            t_stamp = tx.get("timestamp", "N/A")
                            st.code(f"Tx #{idx+1} | Time: {t_stamp} | Signature: {sig}", language="text")
                    else:
                        st.info("No recent transaction signatures retrieved.")
                        
            except Exception as e:
                st.error(f"An error occurred while executing the copilot workflow: {e}")