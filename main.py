import streamlit as st
import os

from modules.auth_manager import check_login, logout_button
from modules.admin_dashboard import render_admin_dashboard
from modules.user_dashboard import render_user_dashboard
from modules.trading_view import render_trading_view
from modules.smc_manual import render_smc_manual
from modules.smc_chart import render_analytical_chart
from modules.smc_vision import render_smc_vision
from modules.smc_execution import render_smc_execution
from modules.news import render_news_ticker

st.set_page_config(
    page_title="Ironclad Capital Partners - SMC",
    page_icon="📈",
    layout="wide"
)

if check_login():
    # 📌 រៀបចំ Header ឱ្យ Logo របស់ Ironclad Capital និង Bull & Bear នៅទន្ទឹមគ្នា
    col_logo, col_bear, col_title = st.columns([0.08, 0.08, 0.84], gap="small")
    
    with col_logo:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=55)
        else:
            st.image("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=100&h=100&fit=crop", width=55)
            
    with col_bear:
        st.image("https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=100&h=100&fit=crop", width=55)
        
    with col_title:
        st.markdown("## **Ironclad Capital Partners - SMC Trading System**")
        st.markdown("<p style='font-size: 12px; color: gray; margin-top: -15px;'>EMPOWERING GROWTH | Institutional Smart Money Concepts (SMC) Signal</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Sidebar
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", use_container_width=True)

    st.sidebar.markdown("<h3 style='text-align: center; margin-bottom: 0px;'>Ironclad Capital</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 11px; color: gray;'>EMPOWERING GROWTH</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    st.sidebar.success("Status: Connected to MT5/API")
    st.sidebar.caption(f"👤 User: {st.session_state.get('username')} ({st.session_state.get('role')})")
    
    st.sidebar.markdown("---")
    logout_button()

    user_role = st.session_state.get('role', 'user')

    if user_role == 'admin':
        st.sidebar.markdown("---")
        st.sidebar.subheader("🧭 Admin Navigation")
        admin_page = st.sidebar.radio("ជ្រើសរើសផ្ទាំង", ["📈 SMC Full Dashboard (Admin)", "🛠️ គ្រប់គ្រងអ្នកប្រើប្រាស់ (User Management)"])
        
        if admin_page == "🛠️ គ្រប់គ្រងអ្នកប្រើប្រាស់ (User Management)":
            render_admin_dashboard()
        else:
            col_charts, col_manual_input = st.columns([1.3, 0.7], gap="medium")
            with col_charts:
                try:
                    render_trading_view()
                except:
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
        render_user_dashboard()
