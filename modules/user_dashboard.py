import streamlit as st
import os
from modules.smc_execution import render_smc_execution

def render_user_dashboard():
    """
    ផ្ទាំង Dashboard សម្រាប់ User ធម្មតា៖ បង្ហាញតែ Welcome និងតម្លៃ Entry, TP, SL ប៉ុណ្ណោះ
    """
    # ១. បង្ហាញ Logo និងឈ្មោះ Ironclad Capital
    col_logo, col_title = st.columns([0.2, 0.8])
    with col_logo:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=100)
    with col_title:
        st.markdown("<h1 style='margin-bottom:0px; color:#DAA520;'>Ironclad Capital</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px; color:gray;'>EMPOWERING GROWTH | Institutional SMC Signals</p>", unsafe_allow_html=True)

    st.markdown("---")

    # ២. បង្ហាញសារ Welcome (ឈ្មោះ User នោះ)
    username = st.session_state.get('username', 'Valued Client')
    st.markdown(f"### 👋 Welcome, **{username}**!")
    st.info("💡 ប្រព័ន្ធកំពុងដំណើរការចាប់សញ្ញាតម្លៃ Buy/Sell, TP និង SL ស្វ័យប្រវត្តិ។ សូមពិនិត្យមើលសញ្ញាខាងក្រោម៖")

    st.markdown("---")

    # ៣. បង្ហាញតែតម្លៃ Buy/Sell, TP, និង SL ពី smc_execution ប៉ុណ្ណោះ
    render_smc_execution()