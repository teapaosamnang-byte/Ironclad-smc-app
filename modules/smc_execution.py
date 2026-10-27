import streamlit as st
import json
import os
import time

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
    """
    ទាញយកតម្លៃ Real-time ស្វ័យប្រវត្តិពី MT5 (ឬ Fallback ករណី Cloud)
    """
    try:
        import MetaTrader5 as mt5
        if mt5.initialize():
            tick = mt5.symbol_info_tick(symbol)
            if tick:
                return (tick.bid + tick.ask) / 2
    except:
        pass
    
    # ករណីរត់លើ Cloud ឬគ្មាន MT5 គឺទាញយកតម្លៃ Simul/Fallback ចុងក្រោយ
    return st.session_state.get('live_price_override', 4008.385)

def evaluate_smc_conditions(current_price, config):
    """
    អនុវត្តរូបមន្ត SMC Analysis ដើម្បីផ្ទៀងផ្ទាត់លក្ខខណ្ឌចូលផ្សារ (Entry Signals)
    """
    big_min = config.get("big_min", 3980.00)
    big_max = config.get("big_max", 4030.00)
    sub_patterns = config.get("sub_patterns", [])

    is_in_big_zone = big_min <= current_price <= big_max
    active_sub = None
    
    for idx, sub in enumerate(sub_patterns):
        if sub.get("min", 0) <= current_price <= sub.get("max", 0):
            active_sub = f"Sub-Pattern {idx+1}"
            break

    # កំណត់ Signal Condition តាមរូបមន្ត SMC
    if is_in_big_zone:
        if active_sub:
            signal = f"🔥 ENTRY CONFIRMED ({active_sub})"
            status_color = "success"
        else:
            signal = "👀 WATCHING ZONE (Inside Big Pattern)"
            status_color = "info"
    elif current_price > big_max:
        signal = "⚠️ OVERBOUGHT / PREMIUM ZONE"
        status_color = "warning"
    else:
        signal = "📉 DISCOUNT ZONE / WAITING"
        status_color = "error"

    return {
        "is_in_zone": is_in_big_zone,
        "active_sub": active_sub,
        "signal": signal,
        "status_color": status_color,
        "big_min": big_min,
        "big_max": big_max
    }

@st.fragment
def render_smc_execution():
    st.markdown("---")
    
    user_role = st.session_state.get('role', 'user')
    config = load_config()
    
    # 1. ទាញយកតម្លៃ Real-time ដោយស្វ័យប្រវត្តិ
    live_price = get_live_market_price("XAUUSD")
    
    # 2. រត់រូបមន្តវិភាគ SMC ស្វ័យប្រវត្តិ
    analysis = evaluate_smc_conditions(live_price, config)

    # ==========================================
    # 👑 ADMIN VIEW (បង្ហាញទិន្នន័យពេញលេញ + Controls)
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
            if analysis['status_color'] == 'success':
                st.success(analysis['signal'])
            elif analysis['status_color'] == 'warning':
                st.warning(analysis['signal'])
            elif analysis['status_color'] == 'info':
                st.info(analysis['signal'])
            else:
                st.error(analysis['signal'])

        with st.expander("🔍 Admin Detailed Pattern Analysis & Sub-Zones", expanded=True):
            st.write(f"- ** Big Pattern Range**: `[{analysis['big_min']:,.2f} - {analysis['big_max']:,.2f}]`")
            st.write(f"- ** Current Trigger Status**: **{analysis['signal']}**")
            
            sub_patterns = config.get("sub_patterns", [])
            for idx, sub in enumerate(sub_patterns):
                s_min, s_max = sub.get("min", 0), sub.get("max", 0)
                hit = "🟢 ACTIVE/HIT" if s_min <= live_price <= s_max else "⚪ Out of Range"
                st.write(f"  - Sub-Pattern {idx+1} `[{s_min:,.2f} - {s_max:,.2f}]`: {hit}")

    # ==========================================
    # 👤 USER VIEW (បង្ហាញតែ Conditions ដែលកំណត់ឱ្យឃើញ)
    # ==========================================
    else:
        st.markdown("### 📊 SMC Market Signals (User View)")
        st.caption("ស្ថានភាពទីផ្សារបច្ចុប្បន្នផ្អែកលើការវិភាគ SMC។")

        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.metric(label="🪙 Current Market Price", value=f"{live_price:,.3f}")
        with col_u2:
            if analysis['is_in_zone']:
                st.success("🟢 Market in Analysis Zone")
            else:
                st.info("⚪ Market Outside Analysis Zone")

        st.info(f"📋 **Market Signal**: {analysis['signal']}")
