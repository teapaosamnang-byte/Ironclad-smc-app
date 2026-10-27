import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from PIL import Image

USER_FILE = "users.csv"

def load_auth_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        # Default Users ពេលមិនទាន់មាន File
        df = pd.DataFrame([
            {"username": "admin", "password": "adminpassword", "role": "admin", "expires_at": "Unlimited"},
            {"username": "user1", "password": "123", "role": "user", "expires_at": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")}
        ])
        df.to_csv(USER_FILE, index=False)
        return df

def check_login():
    df_users = load_auth_users()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""
        st.session_state['role'] = ""

    if not st.session_state['logged_in']:
        # จัดรูปแบบหน้า Login ให้มีความเป็น Professional
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            # ដាក់រូបភាព Bull & Bear ត្រង់ផ្ទាំង Login พร้อมកាត់អក្សរ Bear... ខាងក្រោមចេញ និងបង្រួញទំហំ
            img_path = None
            if os.path.exists("assets/bull&bear"):
                img_path = "assets/bull&bear"
            elif os.path.exists("assets/bull&bear.png"):
                img_path = "assets/bull&bear.png"
                
            if img_path and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    img_width, img_height = img.size
                    # កាត់ផ្នែកខាងក្រោមចេញប្រហែល 40 pixels เพื่อซ่อนคำว่า Bear...
                    if img_height > 40:
                        cropped_img = img.crop((0, 0, img_width, img_height - 40))
                    else:
                        cropped_img = img
                        
                    # បង្ហាញរូបភាពចំកណ្តាលជាមួយទំហំតូចសមរម្យ (width=180)
                    r_col1, r_col2, r_col3 = st.columns([1, 2, 1])
                    with r_col2:
                        st.image(cropped_img, width=180)
                except Exception:
                    pass
                
            st.markdown("<h2 style='text-align: center; color: #DAA520;'>Ironclad Capital - System Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 13px; color: gray;'>Institutional SMC Trading System</p>", unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("ឈ្មោះអ្នកប្រើប្រាស់ (Username)")
                password = st.text_input("ពាក្យសម្ងាត់ (Password)", type="password")
                submit = st.form_submit_button("ចូលប្រព័ន្ធ (Login)")
                
                if submit:
                    user_row = df_users[df_users['username'] == username]
                    
                    if not user_row.empty and str(user_row.iloc[0]['password']) == str(password):
                        role = user_row.iloc[0]['role']
                        expires_at = str(user_row.iloc[0]['expires_at'])
                        
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
