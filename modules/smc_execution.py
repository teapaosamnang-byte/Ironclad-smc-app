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
        "sub_patterns": []
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
    return st.session_state.get('live_price_override', 4022.005)

def evaluate_smc_conditions(current_price, config):
    big_min = config.get("big_min", 3980.00)
    big_max = config.get("big_max", 4030.00)

    # ពិនិត្យថាតើតម្លៃបានចូលដល់ OB Zone ហើយឬยัง
    is_in_ob_zone = big_min <= current_price <= big_max
    
    mid_price = (big_min + big_max) / 2
    
    if current_price < mid_price:
        signal_type = "BUY"
        action = "BUY SIGNAL (DISCOUNT OB)"
        entry = current_price
        sl = big_min - 10.00
        tp = big_max + 20.00
    else:
        signal_type = "SELL"
        action = "SELL SIGNAL (PREMIUM OB)"
        entry = current_price
        sl = big_max + 10.00
        tp = big_min - 20.00

    return {
        "is_in_ob_zone": is_in_ob_zone,
        "signal_type": signal_type,
        "action": action,
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
    # 👑 ADMIN VIEW
    # ==========================================
    if user_role == 'admin':
        st.markdown("### ⚡ SMC Real-time Execution (Admin Dashboard)")
        st.caption("ប្រព័ន្ធតាមដានតម្លៃ Real-time និងរង់ចាំតម្លៃចូលដល់ OB Zone មុននឹងបញ្ជាក់សញ្ញា។")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🪙 XAUUSD Real-time Price", value=f"{live_price:,.3f}")
        with col2:
            st.metric(label="📍 OB Zone Range", value=f"{analysis['big_min']:,.2f} - {analysis['big_max']:,.2f}")
        with col3:
            if analysis['is_in_ob_zone']:
                st.success("🟢 INSIDE OB ZONE")
            else:
                st.warning("⚪ WAITING FOR OB")

        with st.expander("🔍 Admin Detailed Analysis", expanded=True):
            st.write(f"- **Direction**: **{analysis['action']}**")
            st.write(f"- **Entry**: `{analysis['entry']:,.3f}`")
            st.write(f"- **SL**: `{analysis['sl']:,.3f}` | **TP**: `{analysis['tp']:,.3f}`")

    # ==========================================
    # 👤 USER VIEW (បង្ហាញសញ្ញាតែមួយផ្លូវ ពេលតម្លៃចូលដល់ OB Zone ពិតប្រាកដ)
    # ==========================================
    else:
        st.markdown("### 🚨 SMC Trade Signals")
        st.caption("សញ្ញាបញ្ជាទិញលក់ជាក់ស្តែងផ្អែកលើប្រព័ន្ធ SMC ។")

        if analysis['is_in_ob_zone']:
            st.success("🟢 **SIGNAL STATUS: PRICE HIT OB ZONE & CONFIRMED**")
            st.markdown(f"### 🎯 Active Direction: **{analysis['action']}**")
            
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                st.metric(label="📍 Entry Price", value=f"{analysis['entry']:,.3f}")
            with col_u2:
                st.metric(label="🛡️ Stop Loss (SL)", value=f"{analysis['sl']:,.3f}")
            with col_u3:
                st.metric(label="🎯 Take Profit (TP)", value=f"{analysis['tp']:,.3f}")
        else:
            st.info("⚪ **SIGNAL STATUS: WAITING FOR PRICE TO REACH OB ZONE**")
            st.write("តម្លៃបច្ចុប្បន្ននៅក្រៅតំបន់ OB Zone។ ប្រព័ន្ធកំពុងរង់ចាំរហូតដល់តម្លៃចូលដល់ទើបចេញសញ្ញាបញ្ជាក់ជូន។")
