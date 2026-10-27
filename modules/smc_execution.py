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
        "big_min": 4060.00,
        "big_max": 4200.00,
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
    return st.session_state.get('live_price_override', 4009.295)

def evaluate_smc_conditions(current_price, config):
    big_min = config.get("big_min", 4060.00)
    big_max = config.get("big_max", 4200.00)
    sub_patterns = config.get("sub_patterns", [])

    # ពិនិត្យថាតើតម្លៃស្ថិតក្នុង Sub-Pattern ណាមួយដែលបានកំណត់ច្បាស់លាស់ដែរឬទេ
    hit_sub = None
    for sub in sub_patterns:
        if sub.get("min", 0) <= current_price <= sub.get("max", 0):
            hit_sub = sub
            break

    is_in_big_zone = big_min <= current_price <= big_max
    is_confirmed = hit_sub is not None  # ត្រូវតែប៉ះចំ Sub-pattern (OB) ទើបຖືថា Confirm

    mid_price = (big_min + big_max) / 2

    # កំណត់ទិសដៅ Buy ឬ Sell តែមួយផ្លូវច្បាស់លាស់ មិនឱ្យវង្វេង
    if current_price < mid_price:
        signal_type = "BUY"
        action = "BUY SIGNAL (DISCOUNT ZONE)"
        entry = current_price
        sl = big_min - 10.00
        tp = big_max + 20.00
    else:
        signal_type = "SELL"
        action = "SELL SIGNAL (PREMIUM ZONE)"
        entry = current_price
        sl = big_max + 10.00
        tp = big_min - 20.00

    return {
        "is_in_zone": is_in_big_zone,
        "is_confirmed": is_confirmed,
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
        st.caption("ប្រព័ន្ធទាញយកតម្លៃ Real-time និងផ្ទៀងផ្ទាត់តាម Sub-Patterns ស្វ័យប្រវត្តិ។")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🪙 XAUUSD Real-time Price", value=f"{live_price:,.3f}")
        with col2:
            st.metric(label="📍 Big Pattern Range", value=f"{analysis['big_min']:,.2f} - {analysis['big_max']:,.2f}")
        with col3:
            if analysis['is_confirmed']:
                st.success("🟢 OB CONFIRMED")
            else:
                st.warning("⚪ WAITING FOR OB")

        with st.expander("🔍 Admin Detailed Analysis", expanded=True):
            st.write(f"- **Direction**: **{analysis['action']}**")
            st.write(f"- **Entry**: `{analysis['entry']:,.3f}`")
            st.write(f"- **SL**: `{analysis['sl']:,.3f}` | **TP**: `{analysis['tp']:,.3f}`")

    # ==========================================
    # 👤 USER VIEW (បង្ហាញសញ្ញាតែមួយផ្លូវ ពេលតម្លៃចូលដល់ OB Zone)
    # ==========================================
    else:
        st.markdown("### 🚨 SMC Trade Signals")
        st.caption("សញ្ញាបញ្ជាទិញលក់ជាក់ស្តែងផ្អែកលើប្រព័ន្ធ SMC ។")

        if analysis['is_confirmed']:
            st.success("🟢 **SIGNAL STATUS: ORDER BLOCK CONFIRMED**")
            st.markdown(f"### 🎯 Active Direction: **{analysis['action']}**")
            
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                st.metric(label="📍 Entry Price", value=f"{analysis['entry']:,.3f}")
            with col_u2:
                st.metric(label="🛡️ Stop Loss (SL)", value=f"{analysis['sl']:,.3f}")
            with col_u3:
                st.metric(label="🎯 Take Profit (TP)", value=f"{analysis['tp']:,.3f}")
        else:
            st.info("⚪ **SIGNAL STATUS: WAITING FOR PRICE TO HIT ORDER BLOCK (OB)**")
            st.write("តម្លៃបច្ចុប្បន្នមិនទាន់ចូលដល់កម្រិត Order Block ដែលបានកំណត់ទេ។ ប្រព័ន្ធកំពុងតាមដានជាប្រចាំ។")
