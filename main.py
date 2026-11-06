import streamlit as st
from modules.auth_manager import check_login, logout_button
from modules.admin_dashboard import render_admin_dashboard
from modules.user_dashboard import render_user_dashboard
from modules.smc_manual import render_smc_manual

# 1. Page Configuration
st.set_page_config(
    page_title="Ironclad Bot Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Authentication Check & Sidebar Navigation
if check_login():
    st.sidebar.caption(f"👤 Account: {st.session_state.get('username')} ({st.session_state.get('role')})")
    logout_button()
    
    role = st.session_state.get('role')
    
    if role == 'admin':
        # Admin Navigation Menu
        page = st.sidebar.radio("Navigation", ["🛠️ User Management", "📈 SMC Manual Control"])
        if page == "🛠️ User Management":
            render_admin_dashboard()
        else:
            render_smc_manual()
            render_user_dashboard()
    else:
        # Standard User Dashboard Portal
        render_user_dashboard()