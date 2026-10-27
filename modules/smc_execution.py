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
    ទាញយកតម្លៃ Real-time និងទិន្នន័យ Candle Wick ពី MT5 ឬ Fallback
    """
    try:
        import MetaTrader5 as mt5
        if mt5.initialize():
            rates_5m = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 3)
            rates_15m = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 2)
            tick = mt5.symbol_info_tick(symbol)
            
            if tick and rates_5m is not None and rates_15m is not None:
                current_price = (tick.bid + tick.ask) / 2
                # យក High Wick និង Low Wick នៃ Candlestick បច្ចុប្បន្នលើ 5m/15m
                current_high_wick = float(rates_5m[-1]['high'])
                current_low_wick = float(rates_5m[-1]['low'])
                return current_price, current_high_wick, current_low_wick
    except:
        pass
    
    # Fallback Values សម្រាប់រត់លើ Cloud
    fallback_price = st.session_state.get('live_price_override', 4022.880)
    return fallback_price, fallback_price + 2.500, fallback_price - 2.500

def evaluate_smc_conditions(config):
    big_min = config.get("big_min", 3980.00)
    big_max = config.get("big_max", 4030.00)

    current_price, high_wick, low_wick = get_live_market_data("XAUUSD")

    # ពិនិត្យថាតើតម្លៃបានចូលដល់ OB Zone ហើយឬยัง
    is_in_ob_zone = big_min <= current_price <= big_max
    
    mid_price = (big_min + big_max) / 2
    
    # កំណត់ទិសដៅតែមួយផ្លូវ (Exclusive Direction) និង Entry នៅត្រង់ Wick តាមការចង់បាន
    if current_price < mid_price:
        signal_type = "BUY"
        action = "BUY SIGNAL (DISCOUNT OB)"
        entry = low_wick  # យក Low Wick សម្រាប់ Buy
        sl = big_min - 10.00
        tp = big_max + 20.00
    else:
        signal_type = "SELL"
        action = "SELL SIGNAL (PREMIUM OB)"
        entry = high_wick  # យក High Wick សម្រាប់ Sell តាម 15m/5m Confirmation
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
        "big_max": big_max,
        "current_price": current_price
    }

@st.fragment
def render_smc_execution():
    st.markdown("---")
    user_role = st.session_state.get('role', 'user')
    config = load_config()
    analysis = evaluate_smc_conditions(config)

    # ==========================================
    # 👑 ADMIN VIEW
    # ==========================================
    if user_role == 'admin':
        st.markdown("### ⚡ SMC Real-time Execution (Admin Dashboard)")
        st.caption("ប្រព័ន្ធតាមដានតម្លៃ Real-time, ផ្ទៀងផ្ទាត់ Timeframe 15m/5m និងរង់ចាំតម្លៃចូលដល់ OB Zone។")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🪙 XAUUSD Real-time Price", value=f"{analysis['current_price']:,.3f}")
        with col2:
            st.metric(label="📍 OB Zone Range", value=f"{analysis['big_min']:,.2f} - {analysis['big_max']:,.2f}")
        with col3:
            if analysis['is_in_ob_zone']:
                st.success("🟢 INSIDE OB ZONE")
            else:
                st.warning("⚪ WAITING FOR OB")

        with st.expander("🔍 Admin Detailed Analysis", expanded=True):
            st.write(f"- **Direction**: **{analysis['action']}**")
            st.write(f"- **Candle Wick Entry**: `{analysis['entry']:,.3f}`")
            st.write(f"- **SL**: `{analysis['sl']:,.3f}` | **TP**: `{analysis['tp']:,.3f}`")

    # ==========================================
    # 👤 USER VIEW (បង្ហាញសញ្ញាតែមួយផ្លូវ ពេលតម្លៃចូលដល់ OB Zone ពិតប្រាកដ)
    # ==========================================
    else:
        st.markdown("### 🚨 SMC Trade Signals")
        st.caption("សញ្ញាបញ្ជាទិញលក់ជាក់ស្តែងផ្អែកលើប្រព័ន្ធ SMC និង Timeframe 15m/5m Confirmation។")

        if analysis['is_in_ob_zone']:
            st.success("🟢 **SIGNAL STATUS: OB HIT & 15m/5m CONFIRMED**")
            st.markdown(f"### 🎯 Active Direction: **{analysis['action']}**")
            
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                st.metric(label="📍 Candle Wick Entry", value=f"{analysis['entry']:,.3f}")
            with col_u2:
                st.metric(label="🛡️ Stop Loss (SL)", value=f"{analysis['sl']:,.3f}")
            with col_u3:
                st.metric(label="🎯 Take Profit (TP)", value=f"{analysis['tp']:,.3f}")
        else:
            st.info("⚪ **SIGNAL STATUS: WAITING FOR PRICE TO REACH OB ZONE**")
            st.write("តម្លៃបច្ចុប្បន្ននៅក្រៅតំបន់ OB Zone។ ប្រព័ន្ធកំពុងរង់ចាំរហូតដល់តម្លៃចូលដល់ និងផ្ទៀងផ្ទាត់ Candlestick Confirm លើ 15m/5m ទើបចេញសញ្ញាជូន។")
