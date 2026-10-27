import streamlit as st
import os

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        logo_path = "assets/logo.png"
        bullbear_path = "assets/bull&bear.png"
        
        # 📌 ប្រើប្រាស់ CSS Flexbox เพื่อจัดរូបភាពទាំងពីរឱ្យនៅកៀកគ្នា កំរិតទំហំ Height និង Width ឱ្យស្មើគ្នាចំកណ្តាល
        st.markdown(
            """
            <style>
            .login-logo-wrapper {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 15px;
                margin-bottom: 10px;
            }
            .login-logo-wrapper img {
                width: 95px !important;
                height: 95px !important;
                object-fit: contain;
                border-radius: 8px;
            }
            </style>
            
            <div class="login-logo-wrapper">
                <img src="app/static/assets/logo.png" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=100&h=100&fit=crop';">
                <img src="app/static/assets/bull&bear.png" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=100&h=100&fit=crop';">
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<h2 style='text-align: center; margin-top: 10px;'>Ironclad Capital - System Login</h2>", unsafe_allow_html=True)
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
