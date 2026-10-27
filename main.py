import streamlit as st
import os

from modules.auth_manager import check_login, logout_button
from modules.admin_dashboard import render_admin_dashboard
from modules.user_dashboard import render_user_dashboard

# Imports សម្រាប់ Admin Full Dashboard
from modules.trading_view import render_trading_view
from modules.smc_manual import render_smc_manual
from modules.smc_chart import render_analytical_chart
from modules.smc_vision import render_smc_vision
from modules.smc_execution import render_smc_execution
from modules.news import render_news_ticker

# ==========================================
# 🚀 STREAMLIT PAGE CONFIG & LAYOUT SETUP
# ==========================================
st.set_page_config(
    page_title="Ironclad Capital Partners - SMC",
    page_icon="📈",
    layout="wide"
)

# 1. ពិនិត្យការ Login
if check_login():
    
    # 2. SIDEBAR LOGO & INFO
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", use_container_width=True)

    st.sidebar.markdown("<h3 style='text-align: center; margin-bottom: 0px;'>Ironclad Capital</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 11px; color: gray;'>EMPOWERING GROWTH</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    st.sidebar.success("Status: Connected to MT5/API")
    st.sidebar.caption(f"👤 User: {st.session_state.get('username')} ({st.session_state.get('role')})")
    
    # ប៊ូតុង Logout
    st.sidebar.markdown("---")
    logout_button()

    # 3. ROUTING តាមសិទ្ធិ (Role-Based Routing) យ៉ាងដាច់ស្រឡះ
    user_role = st.session_state.get('role', 'user')

    if user_role == 'admin':
        # 👑 សម្រាប់ Admin: មានជម្រើសមើល Full Dashboard ឬ ចូលទៅគ្រប់គ្រង User
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧭 Admin Navigation")
        admin_page = st.sidebar.radio("ជ្រើសរើសផ្ទាំង", ["📈 SMC Full Dashboard (Admin)", "🛠️ គ្រប់គ្រងអ្នកប្រើប្រាស់ (User Management)"])
        
        if admin_page == "🛠️ គ្រប់គ្រងអ្នកប្រើប្រាស់ (User Management)":
            render_admin_dashboard()
        else:
            # ផ្ទាំង Full Dashboard ពេញលេញសម្រាប់ Admin
            col_charts, col_manual_input = st.columns([1.3, 0.7], gap="medium")
            with col_charts:
                try:
                    render_trading_view()
                except Exception as e:
                    st.info("TradingView Component Loading...")
                st.markdown("---")
                render_analytical_chart()

            with col_manual_input:
                render_smc_vision()
                st.markdown("---")
                render_smc_manual()

            st.markdown("---")
            render_smc_execution()
            render_news_ticker()

    else:
        # 👤 សម្រាប់ User ធម្មតា: បង្ហាញតែ User Dashboard (មាន Logo, Welcome និងតម្លៃ Signal ប៉ុណ្ណោះ)
        render_user_dashboard()