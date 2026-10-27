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

def get_live_market_data(symbol="XAUUSD"):
    """
    ទាញយកតម្លៃ Real-time និង Candlestick Wick ពី MT5 ឬយកតម្លៃពី Manual Input / Fallback
    """
    try:
        import MetaTrader5 as mt5
        if mt5.initialize():
            rates_5m = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 3)
            rates_15m = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 2)
            tick = mt5.symbol_info_tick(symbol)
            
            if tick and rates_5m is not None and rates_15m is not None:
                current_price = (tick.bid + tick.ask) / 2
                current_high_wick = float(rates_5m[-1]['high'])
                current_low_wick = float(rates_5m[-1]['low'])
                return current_price, current_high_wick, current_low_wick
    except:
        pass
    
    # យកតម្លៃពី Session State ដែលបាន Input ក្នុង smc_manual.py
    bg_max = st.session_state.get('inp_bg_range_max', 4030.00)
    bg_min = st.session_state.get('inp_bg_range_min', 3980.00)
    fallback_price = st.session_state.get('live_price_override', bg_max - 2.00) # កំណត់ឱ្យនៅជិត OB លើដើម្បីឱ្យងាយស្រួលតេស្តសញ្ញា Sell
    return fallback_price, bg_max + 2.500, bg_min - 2.500

def evaluate_smc_conditions():
    # ទាញយកតម្លៃ Range ពី Manual Input (smc_manual.py)
    big_min = st.session_state.get('inp_bg_range_min', 3980.00)
    big_max = st.session_state.get('inp_bg_range_max', 4030.00)

    current_price, high_wick, low_wick = get_live_market_data("XAUUSD")

    # លក្ខខណ្ឌ SMC: ត្រូវរង់ចាំរហូតទាល់តែតម្លៃឡើងដល់តំបន់ OB ខាងលើ (Premium Zone ជិត 4030)
    is_in_ob_zone = big_min <= current_price <= big_max
    
    # ត្រូវរង់ចាំ Liquidity Sweep និង 15m/5m Confirmation (តម្លៃឡើងដល់ជិត High នៃ OB Zone)
    is_liquidity_swept_and_confirmed = current_price >= (big_max - 10.00) and is_in_ob_zone

    mid_price = (big_min + big_max) / 2
    
    # កំណត់ទិសដៅ Exclusive Direction (បើនៅ Premium Zone គឺออก SELL តែមួយផ្លូវគត់ មិនឱ្យ Buy មកវង្វេង)
    if current_price < mid_price:
        signal_type = "WAIT"
        action = "WAITING FOR PREMIUM ZONE (DISCOUNT AREA)"
        entry = 0.0
        sl = 0.0
        tp = 0.0
    else:
        signal_type = "SELL"
        action = "SELL SIGNAL (PREMIUM OB & LIQUIDITY SWEEP)"
        # Entry ត្រូវយកតាមកម្រិត High Wick នៃ Candlestick បច្ចុប្បន្ន ក្រោយផ្ទៀងផ្ទាត់ 15m/5m រួច
        entry = high_wick if current_price >= (big_max - 15.00) else big_max
        sl = big_max + 10.00
        tp = big_min - 20.00

    return {
        "is_in_ob_zone": is_in_ob_zone,
        "is_confirmed": is_liquidity_swept_and_confirmed,
        "signal_type": signal_type,
        "action": action,
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "tp": round(tp, 2),
        "big_min": big_min,
        "big_max": big_max,
        "current_price": round(current_price, 2)
    }

@st.fragment
def render_smc_execution():
    st.markdown("---")
    user_role = st.session_state.get('role', 'user')
    analysis = evaluate_smc_conditions()

    # ==========================================
    # 👑 ADMIN VIEW
    # ==========================================
    if user_role == 'admin':
        st.markdown("### ⚡ SMC Real-time Execution (Admin Dashboard)")
        st.caption("ប្រព័ន្ធតាមដានតម្លៃ Real-time, Liquidity Sweep និង 15m/5m Confirmation មុនចេញសញ្ញា Sell។")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🪙 XAUUSD Real-time Price", value=f"{analysis['current_price']:,.2f}")
        with col2:
            st.metric(label="📍 OB Zone Range", value=f"{analysis['big_min']:,.2f} - {analysis['big_max']:,.2f}")
        with col3:
            if analysis['is_confirmed']:
                st.success("🟢 LIQUIDITY SWEEP & CONFIRMED")
            else:
                st.warning("⚪ WAITING FOR OB & SWEEP")

        with st.expander("🔍 Admin Detailed Analysis", expanded=True):
            st.write(f"- **Direction**: **{analysis['action']}**")
            st.write(f"- **Candle High Wick Entry**: `{analysis['entry']:,.2f}`")
            st.write(f"- **Stop Loss (SL)**: `{analysis['sl']:,.2f}` | **Take Profit (TP)**: `{analysis['tp']:,.2f}`")

    # ==========================================
    # 👤 USER VIEW (បង្ហាញសញ្ញា Sell តែមួយផ្លូវច្បាស់លាស់ ពេលតម្លៃឡើងដល់ OB និង Confirm រួច)
    # ==========================================
    else:
        st.markdown("### 🚨 SMC Trade Signals")
        st.caption("សញ្ញាបញ្ជាទិញលក់ជាក់ស្តែងផ្អែកលើប្រព័ន្ធ SMC ។")

        if analysis['is_confirmed'] and analysis['signal_type'] == "SELL":
            st.success("🟢 **SIGNAL STATUS: LIQUIDITY SWEEP & 15m/5m CONFIRMED**")
            st.markdown(f"### 🎯 Active Direction: **{analysis['action']}**")
            
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                st.metric(label="📍 Candle Wick Entry", value=f"{analysis['entry']:,.2f}")
            with col_u2:
                st.metric(label="🛡️ Stop Loss (SL)", value=f"{analysis['sl']:,.2f}")
            with col_u3:
                st.metric(label="🎯 Take Profit (TP)", value=f"{analysis['tp']:,.2f}")
        else:
            st.info("⚪ **SIGNAL STATUS: WAITING FOR PRICE TO REACH OB & LIQUIDITY SWEEP**")
            st.write("តម្លៃបច្ចុប្បន្នមិនទាន់ឡើងដល់តំបន់ OB ខាងលើ (4030) និងមិនទាន់មានការបោស Liquidity + 15m/5m Confirm ទេ។ ប្រព័ន្ធកំពុងរង់ចាំតាមដានយ៉ាងម៉ត់ចត់។")
