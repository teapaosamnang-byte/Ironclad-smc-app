import streamlit as st
from datetime import datetime, timedelta

def check_activation():
    # ពិនិត្យមើលថាតើ User បាន activate រួចហើយឬនៅ
    if "is_activated" not in st.session_state:
        st.session_state.is_activated = False
        st.session_state.expiry_date = None

    if st.session_state.is_activated:
        # ពិនិត្យថ្ងៃផុតកំណត់
        if datetime.now() > st.session_state.expiry_date:
            st.warning("⏱️ Serial Number របស់អ្នកបានផុតកំណត់ហើយ សូមបញ្ចូលលេខកូដថ្មី។")
            st.session_state.is_activated = False
            return False
        return True

    # UI សម្រាប់បញ្ចូល Serial
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h2>🔐 ប្រព័ន្ធទាមទារសកម្មភាព (Activation Required)</h2>
            <p>សូមបញ្ចូល Serial Number ដែលទទួលបានពីម្ចាស់ប្រព័ន្ធដើម្បីបន្តការប្រើប្រាស់។</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        serial_input = st.text_input("Serial Number:", type="password")
        
        # កូដគំរូសម្រាប់តេស្ត (អាចកែប្រែភ្ជាប់ជាមួយ Database ពិតប្រាកដ)
        valid_keys = {
            "SMC-GOLD-1M-2026": 30,  # ១ខែ (៣០ថ្ងៃ)
            "SMC-GOLD-3M-2026": 90   # ៣ខែ (៩០ថ្ងៃ)
        }

        if st.button("Activate ឥឡូវនេះ", use_container_width=True):
            if serial_input in valid_keys:
                days = valid_keys[serial_input]
                st.session_state.is_activated = True
                st.session_state.expiry_date = datetime.now() + timedelta(days=days)
                st.success(f"🎉 ជោគជ័យ! ប្រព័ន្ធត្រូវបានបើកដំណើរការរយៈពេល {days} ថ្ងៃ។")
                st.rerun()
            else:
                st.error("❌ Serial Number មិនត្រឹមត្រូវទេ សូមផ្ទៀងផ្ទាត់ម្តងទៀត។")

    return False