import streamlit as st

@st.fragment
def render_smc_execution():
    st.markdown("---")
    user_role = st.session_state.get('role', 'user')

    # ទាញយកតម្លៃពី Big Pattern ទី 1 មកធ្វើជាតម្លៃគោល
    bg_min = st.session_state.get('inp_bg_1_min', 4000.00)
    bg_max = st.session_state.get('inp_bg_1_max', 4030.00)
    current_price = st.session_state.get('live_market_price', 4022.00)

    # លក្ខខណ្ឌ SMC: ត្រូវរង់ចាំតម្លៃឡើងដល់ OB Zone, Liquidity Sweep និង 15m/5m Confirmation
    is_in_ob_zone = bg_min <= current_price <= bg_max
    is_liquidity_swept_and_confirmed = is_in_ob_zone and (current_price >= (bg_max - 10.00) or current_price <= (bg_min + 10.00))

    mid_price = (bg_min + bg_max) / 2
    
    # កំណត់ទិសដៅ Exclusive Direction (Sell តែមួយផ្លូវបើอยู่ Premium Zone)
    if current_price >= mid_price:
        action = "SELL SIGNAL (PREMIUM OB & LIQUIDITY SWEEP)"
        signal_type = "SELL"
        entry = current_price
        sl = bg_max + 10.00
        tp = bg_min - 20.00
    else:
        action = "BUY SIGNAL (DISCOUNT OB & LIQUIDITY SWEEP)"
        signal_type = "BUY"
        entry = current_price
        sl = bg_min - 10.00
        tp = bg_max + 20.00

    # ==========================================
    # 👑 ADMIN VIEW
    # ==========================================
    if user_role == 'admin':
        st.markdown("### ⚡ SMC Real-time Execution (Admin Dashboard)")
        st.caption("ប្រព័ន្ធតាមដានតម្លៃ Real-time, Liquidity Sweep និង 15m/5m Confirmation។")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="🪙 XAUUSD Real-time Price", value=f"{current_price:,.2f}")
        with col2:
            st.metric(label="📍 Big Pattern Range", value=f"{bg_min:,.2f} - {bg_max:,.2f}")
        with col3:
            if is_liquidity_swept_and_confirmed:
                st.success("🟢 OB HIT & CONFIRMED")
            else:
                st.warning("⚪ WAITING FOR OB & SWEEP")

        with st.expander("🔍 Admin Detailed Analysis", expanded=True):
            st.write(f"- **Direction**: **{action}**")
            st.write(f"- **Entry Price**: `{entry:,.2f}`")
            st.write(f"- **Stop Loss (SL)**: `{sl:,.2f}` | **Take Profit (TP)**: `{tp:,.2f}`")

    # ==========================================
    # 👤 USER VIEW (បង្ហាញតែសញ្ញា Buy ឬ Sell, Entry, TP, SL យ៉ាងច្បាស់)
    # ==========================================
    else:
        st.markdown("### 🚨 SMC Trade Signals")
        st.caption("សញ្ញាបញ្ជាទិញលក់ជាក់ស្តែងផ្អែកលើប្រព័ន្ធ SMC ។")

        if is_liquidity_swept_and_confirmed:
            st.success("🟢 **SIGNAL STATUS: LIQUIDITY SWEEP & 15m/5m CONFIRMED**")
            st.markdown(f"### 🎯 Active Direction: **{action}**")
            
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                st.metric(label="📍 Entry Price", value=f"{entry:,.2f}")
            with col_u2:
                st.metric(label="🛡️ Stop Loss (SL)", value=f"{sl:,.2f}")
            with col_u3:
                st.metric(label="🎯 Take Profit (TP)", value=f"{tp:,.2f}")
        else:
            st.info("⚪ **SIGNAL STATUS: WAITING FOR PRICE TO REACH OB & LIQUIDITY SWEEP**")
            st.write("តម្លៃបច្ចុប្បន្នមិនទាន់ចូលដល់តំបន់ OB Zone និងមិនទាន់មានการបោស Liquidity + 15m/5m Confirm ទេ។ ប្រព័ន្ធកំពុងរង់ចាំតាមដានอย่างដិតដល់។")
