import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from modules.auth_manager import load_users, save_users
from modules.smc_manual import render_smc_manual

def render_admin_dashboard():
    st.header("👑 Admin Panel - User Management")
    
    df = load_users()
    st.dataframe(df, use_container_width=True)
    
    tab1, tab2 = st.columns(2)
    
    with tab1:
        st.subheader("➕ Add New User")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password")
        validity = st.selectbox("Validity", ["1M", "3M", "6M"])
        
        if st.button("Create User"):
            if new_username and new_password:
                today = datetime.now()
                months = int(validity.replace("M", ""))
                exp_date = (today + relativedelta(months=months)).strftime("%Y-%m-%d")
                
                new_data = {
                    "username": new_username,
                    "password": new_password,
                    "role": "user",
                    "validity": validity,
                    "expiry_date": exp_date
                }
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                save_users(df)
                st.success(f"User {new_username} created until {exp_date}")
                st.rerun()

    with tab2:
        st.subheader("❌ Delete User")
        user_to_delete = st.selectbox("Select User to Delete", df[df["role"] != "admin"]["username"].tolist())
        if st.button("Delete User"):
            df = df[df["username"] != user_to_delete]
            save_users(df)
            st.warning(f"User {user_to_delete} deleted!")
            st.rerun()