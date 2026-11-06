import streamlit as st
import pandas as pd
import os
import base64

USERS_FILE = "users.csv"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            df = pd.read_csv(USERS_FILE, sep=None, engine='python', skipinitialspace=True)
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            return pd.DataFrame(columns=["username", "password", "role", "validity", "expiry_date"])
    return pd.DataFrame(columns=["username", "password", "role", "validity", "expiry_date"])

def save_users(df):
    df.to_csv(USERS_FILE, index=False)

def img_to_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def check_login():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        # ពង្រីក Column សងខាង [1.5, 3, 1.5] ដើម្បីបង្រួមប្រអប់ Column កណ្តាលឱ្យតូចជាងមុន ១ភាគ៣
        col1, col2, col3 = st.columns([1.5, 3, 1.5])
        
        with col2:
            st.write("")
            
            bull_base64 = img_to_base64("assets/bull&bear.png")
            logo_base64 = img_to_base64("assets/logo.png")
            
            # រក្សាទំហំរូបភាព 115px និងអក្សរ Ironclad Capital ទំហំ 55px នៅចំកណ្តាលយ៉ាងស្អាត
            header_html = f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; width: 100%;">
                <img src="data:image/png;base64,{logo_base64}" width="130" style="border-radius: 8px; display: block;">
                <h1 style="margin: 0; font-weight: bold; font-size: 55px; line-height: 1.1; text-align: center; color: #D4AF37; flex-grow: 1; padding: 0 5px; white-space: nowrap;">Ironclad Capital</h1>
                <img src="data:image/png;base64,{bull_base64}" width="135" style="border-radius: 8px; display: block; margin-top: 15px;">
            </div>
            """
            st.markdown(header_html, unsafe_allow_html=True)
            
            st.markdown("<p style='font-weight: 600; margin-bottom: 2px;'>Username</p>", unsafe_allow_html=True)
            username = st.text_input("Username", label_visibility="collapsed").strip()
            
            st.markdown("<p style='font-weight: 600; margin-top: 12px; margin-bottom: 2px;'>Password</p>", unsafe_allow_html=True)
            password = st.text_input("Password", type="password", label_visibility="collapsed").strip()
            
            st.write("")
            if st.button("Login", use_container_width=True):
                df = load_users()
                
                if df.empty:
                    st.error("User database is empty or file not found!")
                    return False
                    
                user_match = df[(df["username"] == username) & (df["password"] == password)]
                
                if not user_match.empty:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = user_match.iloc[0]["role"]
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        return False
    return True

def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.clear()
        st.rerun()