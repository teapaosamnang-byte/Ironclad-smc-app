import streamlit as st
import json
import os

CONFIG_FILE = "smc_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "big_min": 3980.00,
        "big_max": 4030.00,
        "sub_patterns": [
            {"min": 3980.00, "max": 4005.00},
            {"min": 4005.00, "max": 4030.00}
        ]
    }

def get_live_market_price(symbol="XAUUSD"):
    try:
        import MetaTrader5 as mt5
        if mt5.initialize():
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                return (tick.bid + tick.ask) / 2
    except:
        pass
    return st.session_state.get('live_price_override', 4008.385)

def evaluate_smc_conditions(current_price, config):
    big_min = config.get("big_min", 3980.00)
    big_max = config.get("big_max", 4030.00)
    
    is_in_big_zone = big_min <= current_price <= big_max

    # កំណត់ទិសដៅតែមួយផ្លូវគត់ (Exclusive Direction: BUY or SELL only)
    mid_price = (big_min + big_max) / 2
    
    if current_price < mid_price:
        action = "BUY SIGNAL (DISCOUNT ZONE)"
        signal_type = "BUY"
        entry = current_price
        sl = big_min - 5.00
        tp = big_max + 15.00
    else:
        action = "SELL SIGNAL (PREMIUM ZONE)"
        signal_type = "SELL"
        entry = current_price
        sl = big_max + 5.00
        tp = big_min - 15.00

    return {
        "is_in_zone": is_in_big_zone,
        "action": action,
        "signal_type": signal_type,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "big_min": big_min,
        "big_max": big_max
    }

@st.fragment
def render_smc_execution():
    st.markdown("---")
    user_role = st.session_state.get('role', 'user')
    config = load_config()
    live_price = get_live_market_price("XAUUSD")
    analysis = evaluate_smc_conditions(live_price, config)

    # ==========================================
    # 👑 ADMIN VIEW (បង្ហាញគ្រប់យ៉ាងពេញលេញ)
    # ==========================================
    if user_role == 'admin':
        st.markdown("### ⚡ SMC Real-time Execution (Admin Dashboard)")
        st.caption("ប្រព័ន្ធទាញយកតម្លៃ Real-time និងវិភាគតាម SMC Patterns ដោយស្វ័យប្រវត្តិ។")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🪙 XAUUSD Real-time Price", value=f"{live_price:,.3f}")
        with col2:
            st.metric(label="📍 Active Big Pattern Zone", value=f"{analysis['big_min']:,.2f} - {analysis['big_max']:,.2f}")
        with col3:
            if analysis['is_in_zone']:
                st.success("🟢 INSIDE ZONE")
            else:
                st.warning("⚪ OUTSIDE ZONE")

        with st.expander("🔍 Admin Detailed Analysis", expanded=True):
            st.write(f"- **Direction**: **{analysis['action']}**")
            st.write(f"- **Suggested Entry**: `{analysis['entry']:,.3f}`")
            st.write(f"- **Stop Loss (SL)**: `{analysis['sl']:,.3f}`")
            st.write(f"- **Take Profit (TP)**: `{analysis['tp']:,.3f}`")

    # ==========================================
    # 👤 USER VIEW (បង្ហាញសញ្ញាតែមួយផ្លូវគត់: Buy ឬ Sell ណាមួយច្បាស់លាស់)
    # ==========================================
    else:
        st.markdown("### 🚨 SMC Trade Signals")
        st.caption("សញ្ញាបញ្ជាទិញលក់ជាក់ស្តែងផ្អែកលើប្រព័ន្ធ SMC ។")

        if analysis['is_in_zone']:
            st.success("🟢 **SIGNAL STATUS: ACTIVE ZONE HIT**")
        else:
            st.info("⚪ **SIGNAL STATUS: WAITING FOR ZONE**")

        # បង្ហាញសញ្ញាតែមួយផ្លូវ (BUY ឬ SELL មិនលាយគ្នា)
        st.markdown(f"### 🎯 Active Direction: **{analysis['action']}**")
        
        col_u1, col_u2, col_u3 = st.columns(3)
        with col_u1:
            st.metric(label="📍 Entry Price", value=f"{analysis['entry']:,.3f}")
        with col_u2:
            st.metric(label="🛡️ Stop Loss (SL)", value=f"{analysis['sl']:,.3f}")
        with col_u3:
            st.metric(label="🎯 Take Profit (TP)", value=f"{analysis['tp']:,.3f}")
