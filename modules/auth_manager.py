import streamlit as st
import os

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        logo_path = "assets/logo.png"
        bullbear_path = "assets/bull&bear.png"
        
        # 📌 ប្រើប្រាស់ CSS ដើម្បីកាត់បន្ថយគម្លាត සහ ដាក់រូបទាំងពីរឱ្យមកនៅកៀកគ្នាចំកណ្តាលយ៉ាងស្អាត
        st.markdown(
            """
            <style>
            .login-logo-container {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 10px;
                margin-bottom: -10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # ຈັດ Columns ឱ្យនៅចំកណ្តាលដោយเว้นសងខាង
        col_left, col_img1, col_img2, col_right = st.columns([2.5, 1, 1, 2.5])
        
        with col_img1:
            if os.path.exists(logo_path):
                st.image(logo_path, width=100)
            elif os.path.exists("logo.png"):
                st.image("logo.png", width=100)
                
        with col_img2:
            if os.path.exists(bullbear_path):
                st.image(bullbear_path, width=100)
            elif os.path.exists("bull&bear.png"):
                st.image("bull&bear.png", width=100)

        st.markdown("<h2 style='text-align: center; margin-top: 15px;'>Ironclad Capital - System Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Institutional SMC Trading System</p>", unsafe_allow_html=True)

        # 🔐 រក្សាលក្ខខណ្ឌ Form Login និង Role Check ដើមទាំងអស់យ៉ាងครบถ้วน
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
