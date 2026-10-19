import streamlit as st
import numpy as np
import yfinance as yf

def fetch_default_manual_4h():
    """ទាញយកតម្លៃតាម Timeframe 4H សម្រាប់ធ្វើជាតម្លៃ Default លើកដំបូង"""
    try:
        ticker = yf.Ticker("GC=F")
        df = ticker.history(period="1mo", interval="60m")
        if not df.empty:
            recent = df.tail(40)
            high_val = float(np.max(recent['High'].values))
            low_val = float(np.min(recent['Low'].values))
            current_price = float(df['Close'].values[-1])
            return round(high_val - 6.0, 2), round(high_val, 2), round(low_val, 2), round(low_val + 6.0, 2), current_price
    except Exception:
        pass
    return 4214.40, 4220.40, 4164.50, 4170.50, 4172.50

def check_tf_confirm(tf_str, high_max, low_min):
    """ពិនិត្យមើល Status របស់ Timeframe នីមួយៗតាមទីផ្សារពិតប្រាកដ"""
    try:
        tf_map = {"5M": "5m", "15M": "15m", "1H": "60m", "2H": "60m", "4H": "60m"}
        interval = tf_map.get(tf_str, "15m")
        ticker = yf.Ticker("GC=F")
        df = ticker.history(period="5d", interval=interval)
        if not df.empty:
            recent = df.tail(20)
            current_price = float(df['Close'].values[-1])
            prev_low = float(recent['Low'].values[-2])
            prev_high = float(recent['High'].values[-2])
            curr_low = float(recent['Low'].values[-1])
            curr_high = float(recent['High'].values[-1])

            # Sweep status
            sweep = (curr_low < prev_low and current_price > prev_low) or \
                    (curr_high > prev_high and current_price < prev_high)
            
            # Direction structure
            if current_price > (high_max + low_min) / 2:
                direction = "W-Pattern Accumulation (Bullish Structure)"
            else:
                direction = "M-Pattern Distribution (Bearish Structure)"
            
            status_text = "🟢 ACTIVE (Sweep Confirmed)" if sweep else "⏳ WAITING (Sweep Pending)"
            return direction, status_text
    except Exception:
        pass
    return "M-Pattern Distribution (Bearish Structure)", "⏳ WAITING (Sweep Pending)"

def render_smc_manual():
    st.markdown("""
        <style>
        .manual-bo-box {
            background-color: #1e222d;
            padding: 8px 12px;
            border-radius: 6px;
            margin-bottom: 6px;
            border-left: 4px solid #d4af37;
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
        }
        .manual-zone-sell {
            background-color: rgba(255, 82, 82, 0.12);
            border: 1px solid #ff5252;
            padding: 8px 10px;
            border-radius: 6px;
            margin-bottom: 6px;
            color: #ffffff;
        }
        .manual-zone-buy {
            background-color: rgba(38, 166, 154, 0.12);
            border: 1px solid #26a69a;
            padding: 8px 10px;
            border-radius: 6px;
            color: #ffffff;
        }
        .manual-badge {
            background-color: #2a2e39;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 11px;
            margin-right: 4px;
            color: #ffffff;
        }
        .manual-sl {
            background-color: #d32f2f;
            color: white;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 11px;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.subheader("✍️ Manual SMC Analysis")
        st.markdown("<p style='font-size: 12px; color: #848e9c; margin-bottom: 4px;'>📍 Base Inputs: <b>4H (Fixed Structure)</b></p>", unsafe_allow_html=True)

        k_h_min = "man_h_min_4H"
        k_h_max = "man_h_max_4H"
        k_l_min = "man_l_min_4H"
        k_l_max = "man_l_max_4H"

        if k_h_min not in st.session_state:
            def_h_min, def_h_max, def_l_min, def_l_max, _ = fetch_default_manual_4h()
            st.session_state[k_h_min] = float(def_h_min)
            st.session_state[k_h_max] = float(def_h_max)
            st.session_state[k_l_min] = float(def_l_min)
            st.session_state[k_l_max] = float(def_l_max)

        # 1. ប្រអប់បញ្ចូលតម្លៃ Range តែ 4H មួយប៉ុណ្ណោះ
        st.markdown(f"<span style='font-size: 11px; color: #ff5252;'>🔴 BO (Highest) Range [4H]:</span>", unsafe_allow_html=True)
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            val_h_min = st.number_input("Min H", step=1.0, format="%.2f", key=k_h_min, label_visibility="collapsed")
        with col_h2:
            val_h_max = st.number_input("Max H", step=1.0, format="%.2f", key=k_h_max, label_visibility="collapsed")

        st.markdown(f"<span style='font-size: 11px; color: #26a69a;'>🟢 BO (Lowest) Range [4H]:</span>", unsafe_allow_html=True)
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            val_l_min = st.number_input("Min L", step=1.0, format="%.2f", key=k_l_min, label_visibility="collapsed")
        with col_l2:
            val_l_max = st.number_input("Max L", step=1.0, format="%.2f", key=k_l_max, label_visibility="collapsed")

        st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

        # 2. គណនា Zones, TP និង SL ផ្អែកលើតម្លៃ 4H
        sell_zone_min = round(float(st.session_state[k_h_min]), 2)
        sell_zone_max = round(float(st.session_state[k_h_max]), 2)
        zone_height_sell = sell_zone_max - sell_zone_min
        
        s_tp1 = round(sell_zone_min - (zone_height_sell + 10.0), 2)
        s_tp2 = round(sell_zone_min - (zone_height_sell + 25.0), 2)
        s_sl = round(sell_zone_max + 8.0, 2)

        buy_zone_min = round(float(st.session_state[k_l_min]), 2)
        buy_zone_max = round(float(st.session_state[k_l_max]), 2)
        zone_height_buy = buy_zone_max - buy_zone_min

        b_tp1 = round(buy_zone_max + (zone_height_buy + 10.0), 2)
        b_tp2 = round(buy_zone_max + (zone_height_buy + 25.0), 2)
        b_sl = round(buy_zone_min - 8.0, 2)

        # 3. បង្ហាញលទ្ធផលវិភាគ (Recommendations)
        st.markdown(f"**📋 Manual SMC Data & Recommendations (4H)**")
        
        st.markdown(f"""
            <div class="manual-bo-box">
                🔴 BO (Highest): <span style="color: #ff5252;">{sell_zone_min:.2f} - {sell_zone_max:.2f}</span>
            </div>
            <div class="manual-bo-box" style="border-left-color: #26a69a;">
                🟢 BO (Lowest): <span style="color: #26a69a;">{buy_zone_min:.2f} - {buy_zone_max:.2f}</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="manual-zone-sell">
                <div style="font-size: 12px; font-weight: bold; margin-bottom: 3px; color: #ff5252;">
                    🔴 SELL ZONE: {sell_zone_min:.2f} - {sell_zone_max:.2f}
                </div>
                <div>
                    <span class="manual-badge">TP1: <b>{s_tp1:.2f}</b></span>
                    <span class="manual-badge">TP2: <b>{s_tp2:.2f}</b></span>
                    <span class="manual-sl">SL: {s_sl:.2f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="manual-zone-buy">
                <div style="font-size: 13px; font-weight: bold; margin-bottom: 3px; color: #26a69a;">
                    🟢 BUY ZONE: {buy_zone_min:.2f} - {buy_zone_max:.2f}
                </div>
                <div>
                    <span class="manual-badge">TP1: <b>{b_tp1:.2f}</b></span>
                    <span class="manual-badge">TP2: <b>{b_tp2:.2f}</b></span>
                    <span class="manual-sl">SL: {b_sl:.2f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)

        # 4. បង្ហាញរង់ជ្រើសរើស Timeframe ដើម្បីមើល Direction & Confirm Status ដូចក្នុងរូបថត
        st.write("**⏱️ Check Direction & Confirm Status by TF:**")
        
        if "manual_view_tf" not in st.session_state:
            st.session_state.manual_view_tf = "4H"

        tfs = ["5M", "15M", "1H", "2H", "4H"]
        cols_tf = st.columns(5)
        for i, tf_name in enumerate(tfs):
            with cols_tf[i]:
                btn_type = "primary" if st.session_state.manual_view_tf == tf_name else "secondary"
                if st.button(tf_name, key=f"v_tf_{tf_name}", type=btn_type, use_container_width=True):
                    st.session_state.manual_view_tf = tf_name
                    st.rerun()

        selected_tf = st.session_state.manual_view_tf
        dir_text, confirm_text = check_tf_confirm(selected_tf, sell_zone_max, buy_zone_min)

        # បង្ហាញទម្រង់ដូចក្នុងរូបភាព ១០០%
        st.markdown(f"""
            <div style="font-size: 13px; color: #d1d4dc; margin-top: 6px;">
                • <b>Direction (Pivot Pattern) [{selected_tf}]:</b> <span style="color: #d4af37;">{dir_text}</span>
            </div>
            <div style="font-size: 13px; color: #d1d4dc; margin-top: 4px;">
                • <b>Confirm Status [{selected_tf}]:</b> {confirm_text}
            </div>
        """, unsafe_allow_html=True)