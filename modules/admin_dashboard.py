import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

USER_FILE = "users.csv"

def load_users_db():
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

def save_users_db(df):
    df.to_csv(USER_FILE, index=False)

def render_admin_dashboard():
    st.title("👑 ផ្ទាំងគ្រប់គ្រងប្រព័ន្ធ (Admin Control Panel)")
    st.write(f"👤 អ្នកគ្រប់គ្រង: **{st.session_state.get('username', 'admin')}**")
    st.markdown("---")
    
    # ផ្ទុកទិន្នន័យពី File CSV ថេរ
    df_users = load_users_db()
    
    st.subheader("📋 បញ្ជីឈ្មោះអ្នកប្រើប្រាស់ទាំងអស់ (Users List)")
    st.dataframe(df_users, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ➕ បន្ថែម User ថ្មី")
        with st.form("add_user_form"):
            new_user = st.text_input("ឈ្មោះថ្មី (New Username)")
            new_pass = st.text_input("ពាក្យសម្ងាត់ថ្មី (New Password)", type="password")
            new_role = st.selectbox("សិទ្ធិ (Role)", ["user", "admin"])
            duration_months = st.selectbox("សុពលភាព (Validity Duration ជាខែ)", [1, 3, 6, 12])
            
            add_submit = st.form_submit_button("💾 រក្សាទុក User (Save)")
            if add_submit:
                if new_user and new_pass:
                    if new_user in df_users['username'].values:
                        st.warning("⚠️ ឈ្មោះអ្នកប្រើប្រាស់នេះមានរួចហើយ!")
                    else:
                        if new_role == "admin":
                            expires_str = "Unlimited"
                        else:
                            exp_date = datetime.now() + timedelta(days=int(duration_months) * 30)
                            expires_str = exp_date.strftime("%Y-%m-%d")
                        
                        new_row = pd.DataFrame([{
                            "username": new_user, 
                            "password": new_pass, 
                            "role": new_role, 
                            "expires_at": expires_str
                        }])
                        df_users = pd.concat([df_users, new_row], ignore_index=True)
                        save_users_db(df_users)
                        st.success(f"✅ បានរក្សាទុក User '{new_user}' ចូលក្នុង System ជោគជ័យ!")
                        st.rerun()
                else:
                    st.error("⚠️ សូមបញ្ចូលឈ្មោះ និងពាក្យសម្ងាត់ឱ្យបានត្រឹមត្រូវ!")

    with col2:
        st.markdown("### 🔑 ប្ដូរ Password")
        with st.form("change_password_form"):
            target_user = st.selectbox("ជ្រើសរើស User ដែលត្រូវប្ដូរ", df_users['username'].tolist())
            new_password = st.text_input("ពាក្យសម្ងាត់ថ្មី (New Password)", type="password")
            change_submit = st.form_submit_button("💾 រក្សាទុក Password (Save)")
            
            if change_submit:
                if new_password:
                    df_users.loc[df_users['username'] == target_user, 'password'] = new_password
                    save_users_db(df_users)
                    st.success(f"✅ បានប្ដូរ និងរក្សាទុក Password របស់ '{target_user}' ជោគជ័យ!")
                    st.rerun()
                else:
                    st.error("⚠️ សូមបញ្ចូលពាក្យសម្ងាត់ថ្មី!")

    with col3:
        st.markdown("### 🗑️ លុប User")
        with st.form("delete_user_form"):
            user_to_delete = st.selectbox("ជ្រើសរើស User ដែលត្រូវលុប", df_users['username'].tolist(), key="del_select")
            del_submit = st.form_submit_button("លុប User")
            if del_submit:
                if user_to_delete == "admin":
                    st.error("❌ មិនអាចលុប Account Admin គោលបានទេ!")
                else:
                    df_users = df_users[df_users['username'] != user_to_delete].reset_index(drop=True)
                    save_users_db(df_users)
                    st.success(f"✅ បានលុប User '{user_to_delete}' រួចរាល់!")
                    st.rerun()
