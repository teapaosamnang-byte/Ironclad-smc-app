import streamlit as st
import os
from modules.smc_analysis import get_technical_signals

# ប្រើប្រាស់ st.fragment(run_every=2) ដើម្បីឱ្យតម្លៃ Live Price និង Signal ធ្វើបច្ចុប្បន្នភាពរៀងរាល់ ២វិនាទីម្តង
@st.fragment(run_every=2)
def render_realtime_signal_portal():
    # ទាញយកទិន្នន័យពី module SMC Analysis (ដែលភ្ជាប់ជាមួយ MT5 Real-time tick)
    data = get_technical_signals("XAUUSD")
    
    # 1. បង្ហាញតម្លៃ Live Price ឱ្យដើរទាន់ទីផ្សារពិត
    st.metric(label="Live Price (XAUUSD)", value=f"{data['current_price']:.3f}")
    
    # 2. បង្ហាញ Signal (BUY / SELL / WAIT) តាម Logic ដើម
    color = "green" if data["signal"] == "BUY" else ("red" if data["signal"] == "SELL" else "orange")
    st.markdown(f"### Signal: <span style='color:{color};'>{data['signal']}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 3. បង្ហាញ Recommended Parameters (Entry, SL, TP1, TP2)
    st.subheader("🎯 Recommended Parameters")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Entry Price", f"{data['entry']:.3f}")
    col2.metric("Stop Loss (SL)", f"{data['sl']:.3f}")
    col3.metric("Take Profit 1 (TP1)", f"{data['tp1']:.3f}")
    col4.metric("Take Profit 2 (TP2)", f"{data['tp2']:.3f}")


def render_user_dashboard():
    # 1. ដាក់ Logo ទំហំធំ (width=110) និងអក្សរ Ironclad Capital ពណ៌មាស
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
    
    col_logo, col_title = st.columns([0.12, 0.88])
    
    with col_logo:
        if os.path.exists(logo_path):
            st.image(logo_path, width=110)
        else:
            st.markdown("🛡️")
            
    with col_title:
        st.markdown(
            "### <span style='color: #D4AF37;'>Ironclad Capital</span> — Client Trading Signal Portal", 
            unsafe_allow_html=True
        )

    # 2. ពិនិត្យសិទ្ធិ: បើជា admin គឺមិនបាច់បង្ហាញសារស្វាគមន៍ និង Disclaimer ទេ
    username = st.session_state.get("username", "Trader")
    
    if username.lower() != "admin":
        st.markdown(f"🙏 **សួស្ដី, {username}!** សូមស្វាគមន៍មកកាន់ប្រព័ន្ធវិភាគសញ្ញាទីផ្សារទាន់ហេតុការណ៍។")
        
        # 🛡️ បន្ថែមផ្នែក System Rules & Risk Philosophy
        with st.expander("🛡️ System Rules & Risk Philosophy (គោលការណ៍ និងវិន័យការពារប្រព័ន្ធ)", expanded=False):
            st.markdown("""
            * **🎯 Strict Trend-Following:** តាមដាន និងចាប់យកតែសញ្ញាស្របតាមទិសដៅធំ (H4 Macro Trend) ប៉ុណ្ណោះ ដើម្បីជៀសវាងការជួប Trend Counter-trend Fakeouts។
            * **🛑 Anti-Fakeout Protection:** រង់ចាំការបញ្ជាក់ពីទៀន M5 និងការលូកយក Liquidity (Sweep) យ៉ាងតឹងរឹង មុននឹងចេញសញ្ញា Trade ជាមួយ Fixed Entry Price។
            * **💰 Long-term Risk Management:** គ្រប់គ្រងទុន និងលុបបំបាត់អារម្មណ៍ផ្ទាល់ខ្លួន (Emotional Trading) ដើម្បីធានាស្ថិរភាពក្នុងការទប់ស្កាត់ហានិភ័យរយៈពេលវែង។
            """)

        st.info(
            "⚠️ **ចំណាំសំខាន់ (Disclaimer):** រាល់សញ្ញា (Signals) និងប៉ារ៉ាម៉ែត្រទាំងអស់ខាងក្រោម "
            "គឺជាការវិភាគព្យាករណ៍តាមប្រព័ន្ធស្វ័យប្រវត្តិ (SMC Analysis) និងជាជំនួយក្នុងការសម្រេចចិត្តប៉ុណ្ណោះ។ "
            "ការជួញដូរទីផ្សារហិរញ្ញវត្ថុមានហានិភ័យខ្ពស់ សូមគ្រប់គ្រងទឹកប្រាក់ និងហានិភ័យ (Risk Management) ឱ្យបានហ្មត់ចត់ជានិច្ច។"
        )
        st.markdown("---")
    else:
        st.write("")

    # 3. ហៅប្រើប្រាស់ Real-time Fragment សម្រាប់ Live Price និង Signal Parameters
    render_realtime_signal_portal()