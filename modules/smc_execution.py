import streamlit as st
import time

def render_smc_execution():
    st.markdown("---")
    
    # ពិនិត្យសិទ្ធិ៖ ផ្ដល់សិទ្ធិឱ្យតែ Admin មើលឃើញផ្នែកនេះប៉ុណ្ណោះ
    user_role = st.session_state.get('role', 'user')
    if user_role != 'admin':
        return  # ប្រសិនបើជា User ធម្មតា គឺមិនបង្ហាញអ្វីទាំងអស់នៅត្រង់នេះ
    
    st.markdown("### ⚡ SMC Real-time Execution & Price Monitor (Admin View)")
    st.caption("ផ្ទាំងសម្រាប់ Admin តាមដានតម្លៃទីផ្សារបច្ចុប្បន្ន និងផ្ទៀងផ្ទាត់ជាមួយ Zone ក្នុងពេលជាក់ស្តែង។")

    # បង្កើត Container សម្រាប់បង្ហាញតម្លៃ Live Price របស់ Admin
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="🪙 XAUUSD Live Price", value="3,994.92", delta="-22.27 (-0.55%)")
    
    with col2:
        # ទាញយកតម្លៃ Min/Max ដែលបានកំណត់ក្នុង Session ឬ Config មកបង្ហាញដើម្បីងាយស្រួលផ្ទៀងផ្ទាត់
        min_zone = st.session_state.get('inp_bg_range_min', 4000.00)
        max_zone = st.session_state.get('inp_bg_range_max', 4250.00)
        st.metric(label="📍 Active Zone Range", value=f"{min_zone} - {max_zone}")

    with col3:
        # ស្ថានភាពផ្ទៀងផ្ទាត់តម្លៃជាមួយ Zone
        current_p = 3994.92
        if min_zone <= current_p <= max_zone:
            st.success("🟢 Price is INSIDE Zone (Ready/Hit)")
        else:
            st.warning("🟡 Waiting for Price to Reach Zone")

    # ផ្នែកសម្រាប់ Admin ចុច Test Trigger ឬ Execution បន្ថែមតាមតម្រូវការ
    with st.expander("🛠️ Admin Advanced Execution Controls", expanded=False):
        st.write("គ្រប់គ្រងការតភ្ជាប់ MT5 និងការបញ្ជូនសញ្ញាแจ้งเตือน (Signals) ជូន Admin៖")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Check MT5 Connection", use_container_width=True):
                st.success("✅ MT5 Connected Successfully (Simulation Active)!")
        with col_btn2:
            if st.button("🚀 Trigger Manual Signal Check", use_container_width=True):
                st.info("ℹ️ បានពិនិត្យរួចរាល់៖ តម្លៃបច្ចុប្បន្នស្ថិតក្នុងកម្រិតត្រួតពិនិត្យ។")
