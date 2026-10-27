import streamlit as st
import os

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        # 📌 ប្រើប្រាស់ HTML/CSS ដើម្បីដាក់រូបទាំងពីរឱ្យនៅកៀកគ្នាចំកណ្តាល និងទំហំធ្មេចសមរម្យ
        logo_path = "assets/logo.png"
        bullbear_path = "assets/bull&bear.png"
        
        # បង្កើត Container จัดกึ่งกลาง
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 10px;">
            """, 
            unsafe_allow_html=True
        )
        
        # ប្រើ Streamlit columns ខាងក្នុង container ជាមួយទំហំ width 150px (ធំជាងមុនបន្តិច និងស្មើគ្នា)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("<div style='display: flex; justify-content: flex-end;'>", unsafe_allow_html=True)
            if os.path.exists(logo_path):
                st.image(logo_path, width=140)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div style='display: flex; justify-content: flex-start;'>", unsafe_allow_html=True)
            if os.path.exists(bullbear_path):
                st.image(bullbear_path, width=140)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center; margin-top: 10px;'>Ironclad Capital - System Login</h2>", unsafe_allow_html=True)
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
