import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

def init_auth_db():
    if 'users_db' not in st.session_state:
        st.session_state['users_db'] = pd.DataFrame([
            {"username": "admin", "password": "adminpassword", "role": "admin", "expires_at": "Unlimited"},
            {"username": "user1", "password": "123", "role": "user", "expires_at": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}
        ])

def check_login():
    init_auth_db()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['role'] = ""

    if not st.session_state['logged_in']:
        # จัดรูปแบบหน้า Login ให้มีความเป็น Professional
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            # ដាក់រូបភាព Bull & Bear ត្រង់ផ្ទាំង Login ដំបូង
            if os.path.exists("assets/bull&bear"):
                st.image("assets/bull&bear", use_container_width=True)
            elif os.path.exists("assets/bull&bear.png"):
                st.image("assets/bull&bear.png", use_container_width=True)
                
            st.markdown("<h2 style='text-align: center; color: #DAA520;'>Ironclad Capital - System Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 13px; color: gray;'>Institutional SMC Trading System</p>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("ឈ្មោះអ្នកប្រើប្រាស់ (Username)")
                password = st.text_input("ពាក្យសម្ងាត់ (Password)", type="password")
                submit = st.form_submit_button("ចូលប្រព័ន្ធ (Login)")
                
                if submit:
                    df_users = st.session_state['users_db']
                    user_row = df_users[df_users['username'] == username]
                    
                    if not user_row.empty and user_row.iloc[0]['password'] == password:
                        role = user_row.iloc[0]['role']
                        expires_at = user_row.iloc[0]['expires_at']
                        
                        if role != "admin" and expires_at != "Unlimited":
                            exp_date = datetime.strptime(expires_at, "%Y-%m-%d")
                            if datetime.now() > exp_date:
                                st.error("❌ គណនីរបស់អ្នកបានផុតកំណត់ការប្រើប្រាស់ហើយ! សូមទាក់ទង Admin។")
                                return False

                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.session_state['role'] = role
                        st.rerun()
                    else:
                        st.error("❌ ឈ្មោះអ្នកប្រើប្រាស់ ឬ ពាក្យសម្ងាត់មិនត្រឹមត្រូវទេ!")
        return False
    return True

def logout_button():
    if st.sidebar.button("🚪 ចាកចេញ (Logout)", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['role'] = ""
        st.rerun()