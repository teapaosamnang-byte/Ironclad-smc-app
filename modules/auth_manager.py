import streamlit as st
import os

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        # 📌 ដាក់ Logo ទាំងពីរទន្ទឹមគ្នាដោយទាញចេញពី Folder assets តាមឈ្មោះពិតប្រាកដ
        col_l1, col_l2 = st.columns([1, 1], gap="small")
        
        with col_l1:
            if os.path.exists("assets/logo.png"):
                st.image("assets/logo.png", width=120)
                
        with col_l2:
            # ប្រើឈ្មោះ "assets/bull&bear.png" ឱ្យត្រូវចំតាម GitHub ของបង
            if os.path.exists("assets/bull&bear.png"):
                st.image("assets/bull&bear.png", width=120)

        st.markdown("<h2 style='text-align: center;'>Ironclad Capital - System Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Institutional SMC Trading System</p>", unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("ឈ្មោះអ្នកប្រើប្រាស់ (Username)")
            password = st.text_input("ពាក្យសម្ងាត់ (Password)", type="password")
            submit = st.form_submit_button("ចូលប្រព័ន្ធ (Login)", use_container_width=True)

            if submit:
                if username == "admin" and password == "admin123":
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['role'] = 'admin'
                    st.success("✅ Login Successful!")
                    st.rerun()
                elif username == "user" and password == "user123":
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['role'] = 'user'
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("⚠️ Username ឬ Password មិនត្រឹមត្រូវទេ!")
        return False
    return True

def logout_button():
    if st.button("🚪 ចាកចេញពីប្រព័ន្ធ (Logout)", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['role'] = None
        st.rerun()
