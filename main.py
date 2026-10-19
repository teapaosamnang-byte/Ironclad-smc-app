import streamlit as st

from modules.auth import check_activation
from modules.trading_view import render_trading_view
from modules.smc_analysis import render_smc_analysis
from modules.smc_manual import render_smc_manual
from modules.news_module import render_news_module

st.set_page_config(
    page_title="Ironclad Capital Partners - SMC",
    page_icon="📊",
    layout="wide"
)

if not check_activation():
    st.stop()

with st.sidebar:
    try:
        st.image("assets/logo.png", width=200)
    except Exception:
        st.title("IRONCLAD CAPITAL")

    st.markdown("### Navigation Menu")
    menu = st.radio(
        "ជ្រើសរើសជម្រើស:",
        ["Dashboard & SMC", "News Analysis", "អំពីពួកយើង"]
    )

    st.divider()
    st.caption("🟢 Status: Connected to MT5/API")
    st.caption("📌 Version: 1.0.0 Pro")
    
    if st.button("🔒 ចាកចេញ (Logout)", use_container_width=True):
        st.session_state.is_activated = False
        st.rerun()

if menu == "Dashboard & SMC":
    st.title("📊 Dashboard & SMC Analysis")

    # បែងចែក Column ជា ២ មេ (ខាងឆ្វេងសម្រាប់ Chart + Manual SMC, ខាងស្តាំសម្រាប់ Auto SMC)
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        # ផ្នែកខាងឆ្វេងផ្នែកខាងលើ៖ Live Chart
        render_trading_view()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ផ្នែកខាងឆ្វេងផ្នែកខាងក្រោម៖ Manual SMC Analysis (ដាក់ជាប់ក្រោម Live Chart តែម្តង)
        render_smc_manual()

    with col_right:
        # ផ្នែកខាងស្តាំ៖ Auto SMC Analysis (រក្សាទុកធម្មតា)
        render_smc_analysis()

elif menu == "News Analysis":
    st.title("📰 Financial & Geopolitical News")
    render_news_module()

elif menu == "អំពីពួកយើង":
    st.title("ℹ️ អំពី Ironclad Capital Partners")
    st.write("ប្រព័ន្ធវិភាគទីផ្សារ Gold/XAUUSD ដោយប្រើប្រាស់ Smart Money Concepts (SMC) Strategy។")