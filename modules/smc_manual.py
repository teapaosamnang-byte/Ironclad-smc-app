import streamlit as st
import json
import os

CONFIG_FILE = "smc_config.json"

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {
        "big_min": 3980.00,
        "big_max": 4030.00,
        "sub_patterns": []
    }

def render_smc_manual():
    st.markdown("### 📝 SMC Manual Input Panel")
    st.caption("បញ្ចូលតម្លៃ SMC Liquidity Zones និង OB Zone យ៉ាងแม่นยำ។")

    config = load_config()

    with st.form("manual_ob_form"):
        col1, col2 = st.columns(2)
        with col1:
            manual_min = st.number_input("OB Zone Minimum (Low)", value=float(config.get("big_min", 3980.00)), step=1.00, format="%.2f", key="inp_bg_range_min")
        with col2:
            manual_max = st.number_input("OB Zone Maximum (High)", value=float(config.get("big_max", 4030.00)), step=1.00, format="%.2f", key="inp_bg_range_max")

        submitted = st.form_submit_button("💾 រក្សាទុក OB Zone (Save)", use_container_width=True)
        if submitted:
            config_data = {
                "big_min": manual_min,
                "big_max": manual_max,
                "sub_patterns": []
            }
            save_config(config_data)
            st.success("✅ បានរក្សាទុក OB Zone ចូល GitHub Storage ជោគជ័យ!")
            st.rerun()

    if os.path.exists(CONFIG_FILE):
        st.write(f"📌 **Current Stored OB Range**: `{config.get('big_min', 0):,.2f} - {config.get('big_max', 0):,.2f}`")
