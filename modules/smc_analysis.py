import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

def fetch_gold_data(interval_str):
    
    try:
        tf_map = {
            "5M": "5m",
            "15M": "15m",
            "1H": "60m",
            "2H": "60m",
            "4H": "60m"
        }
        interval = tf_map.get(interval_str, "15m")
        period = "5d" if interval in ["5m", "15m"] else "1mo"
        
        ticker = yf.Ticker("GC=F")
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return None
        return df
    except Exception:
        return None

def calculate_smc(df):
    
    if df is None or len(df) < 10:
        return None

    recent_df = df.tail(40)
    highs = recent_df['High'].values
    lows = recent_df['Low'].values
    closes = recent_df['Close'].values

  
    bo_top_max = float(np.max(highs))
    bo_top_min = float(bo_top_max - 6.0)
    
    bo_bot_min = float(np.min(lows))
    bo_bot_max = float(bo_bot_min + 6.0)

    current_price = float(closes[-1])
    prev_low = float(lows[-2])
    prev_high = float(highs[-2])
    curr_low = float(lows[-1])
    curr_high = float(highs[-1])

   
    candle_sweep = (curr_low < prev_low and current_price > prev_low) or \
                   (curr_high > prev_high and current_price < prev_high)

    buy_zone_min = round(bo_bot_min, 2)
    buy_zone_max = round(bo_bot_max, 2)
    buy_tp1 = round(buy_zone_max + 12.0, 2)
    buy_tp2 = round(buy_zone_max + 25.0, 2)
    buy_sl = round(buy_zone_min - 8.0, 2)

    sell_zone_min = round(bo_top_min, 2)
    sell_zone_max = round(bo_top_max, 2)
    sell_tp1 = round(sell_zone_min - 12.0, 2)
    sell_tp2 = round(sell_zone_min - 25.0, 2)
    sell_sl = round(sell_zone_max + 8.0, 2)

    if current_price > (bo_top_max + bo_bot_min) / 2:
        direction = "W-Pattern Accumulation (Bullish Structure)"
    else:
        direction = "M-Pattern Distribution (Bearish Structure)"

    return {
        "bo_top": f"{bo_top_min:.2f} - {bo_top_max:.2f}",
        "bo_bottom": f"{bo_bot_min:.2f} - {bo_bot_max:.2f}",
        "sell_zone": f"{sell_zone_min:.2f} - {sell_zone_max:.2f}",
        "sell_tp1": f"{sell_tp1:.2f}",
        "sell_tp2": f"{sell_tp2:.2f}",
        "sell_sl": f"{sell_sl:.2f}",
        "buy_zone": f"{buy_zone_min:.2f} - {buy_zone_max:.2f}",
        "buy_tp1": f"{buy_tp1:.2f}",
        "buy_tp2": f"{buy_tp2:.2f}",
        "buy_sl": f"{buy_sl:.2f}",
        "direction": direction,
        "sweep": candle_sweep,
        "current_price": round(current_price, 2)
    }

def render_smc_analysis():
    st.markdown("""
        <style>
        .bo-box {
            background-color: #1e222d;
            padding: 12px 18px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 5px solid #d4af37;
            font-size: 18px;
            font-weight: bold;
            color: #ffffff;
        }
        .zone-card-sell {
            background-color: rgba(255, 82, 82, 0.12);
            border: 1px solid #ff5252;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 12px;
            color: #ffffff;
        }
        .zone-card-buy {
            background-color: rgba(38, 166, 154, 0.12);
            border: 1px solid #26a69a;
            padding: 15px;
            border-radius: 10px;
            color: #ffffff;
        }
        .badge-tag {
            background-color: #2a2e39;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 13px;
            margin-right: 8px;
        }
        .sl-tag {
            background-color: #d32f2f;
            color: white;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("📊 Smart Money Concepts (SMC) Analysis Dashboard")
    st.markdown("---")
    
    st.write("**⏱️ Select Timeframe:**")
    
    if "current_tf" not in st.session_state:
        st.session_state.current_tf = "15M"

    tfs = ["5M", "15M", "1H", "2H", "4H"]
    cols = st.columns(5)
    
    for i, tf_name in enumerate(tfs):
        with cols[i]:
            btn_type = "primary" if st.session_state.current_tf == tf_name else "secondary"
            if st.button(tf_name, key=f"tf_{tf_name}", type=btn_type, use_container_width=True):
                st.session_state.current_tf = tf_name
                st.rerun()

    tf = st.session_state.current_tf

    with st.spinner(f"🔄 កំពុងទាញយកទិន្នន័យ SMC ស្វ័យប្រវត្តិនៃ Timeframe {tf}..."):
        df = fetch_gold_data(tf)
        smc_res = calculate_smc(df)

    if smc_res is None:
        st.warning("⚠️ មិនអាចទាញយកទិន្នន័យផ្សារផ្ទាល់បានទេ! សូមពិនិត្យសេវាអ៊ីនធឺណិត។")
        return

    st.info(f"📍 វិភាគស្វ័យប្រវត្តិលើ **{tf}** | តម្លៃមាសបច្ចុប្បន្ន: **${smc_res['current_price']}**")

    with st.container():
        st.markdown(f"### 📋 Auto SMC Analysis Data & Recommendations ({tf})")
        
        st.markdown(f"""
            <div class="bo-box">
                🔴 BO (Top): <span style="color: #ff5252;">{smc_res['bo_top']}</span>
            </div>
            <div class="bo-box" style="border-left-color: #26a69a;">
                🟢 BO (Bottom): <span style="color: #26a69a;">{smc_res['bo_bottom']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<b>• Recommendation (Zones, TP & SL):</b>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="zone-card-sell">
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: #ff5252;">
                    🔴 SELL ZONE: {smc_res['sell_zone']}
                </div>
                <div>
                    <span class="badge-tag">TP1: <b>{smc_res['sell_tp1']}</b></span>
                    <span class="badge-tag">TP2: <b>{smc_res['sell_tp2']}</b></span>
                    <span class="sl-tag">SL: {smc_res['sell_sl']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="zone-card-buy">
                <div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color: #26a69a;">
                    🟢 BUY ZONE: {smc_res['buy_zone']}
                </div>
                <div>
                    <span class="badge-tag">TP1: <b>{smc_res['buy_tp1']}</b></span>
                    <span class="badge-tag">TP2: <b>{smc_res['buy_tp2']}</b></span>
                    <span class="sl-tag">SL: {smc_res['buy_sl']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.write(f"**• Direction (Pivot Pattern):** `{smc_res['direction']}`")
        
        if smc_res["sweep"]:
            st.write("**• Confirm Status:** 🟢 **`ACTIVE`** (Candle Sweep Confirmed)")
        else:
            st.write("**• Confirm Status:** ⏳ **`WAITING`** (Sweep Pending)")
