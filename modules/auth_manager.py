import streamlit as st
import os

def check_login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        logo_path = "assets/logo.png"
        bullbear_path = "assets/bull&bear.png"
        
        # 📌 ប្រើប្រាស់ CSS Flexbox ដាក់រូបទាំងពីរឱ្យមកជិតគ្នាចំកណ្តាល និងកំណត់ទំហំឱ្យស្មើគ្នា
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 10px;">
            """,
            unsafe_allow_html=True
        )
        
        # បង្ហាញរូបទី ១ (Logo)
        if os.path.exists(logo_path):
            st.markdown(f'<img src="app/static/{logo_path}" width="120" style="border-radius: 8px;">', unsafe_allow_html=True) # បើសិនជាបង្ហាញតាម HTML មិនចេញ អាចប្រើ st.image ជាមួយ container
            
        # វិធីសាស្ត្រប្រើ st.image ក្នុង Streamlit Container ឱ្យនៅកៀកគ្នា
        col_center1, col_center2 = st.columns([0.15, 0.15], gap="small")
        # លុបចោល columns ធម្មតា ហើយជំនួសដោយ CSS Container វិញ ដើម្បីភាពแน่นอน
        
        st.markdown("</div>", unsafe_allow_html=True)

        # 🎯 ប្រើប្រាស់វិធីសាស្ត្រដ៏ងាយស្រួល និងត្រូវ១០០% ជាមួយ Streamlit Columns ចង្អៀត
        c_space1, c_img1, c_img2, c_space2 = st.columns([2, 1, 1, 2])
        
        with c_img1:
            if os.path.exists(logo_path):
                st.image(logo_path, width=130)
        with c_img2:
            if os.path.exists(bullbear_path):
                st.image(bullbear_path, width=130)

        st.markdown("<h2 style='text-align: center; margin-top: 15px;'>Ironclad Capital - System Login</h2>", unsafe_allow_html=True)
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
