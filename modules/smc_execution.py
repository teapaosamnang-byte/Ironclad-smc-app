import streamlit as st
import json
import os

CONFIG_FILE = "smc_config.json"

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
        "sub_patterns": [
            {"min": 3980.00, "max": 4005.00},
            {"min": 4005.00, "max": 4030.00}
        ]
    }

def render_smc_execution():
    st.markdown("---")
    
    # ពិនិត្យសិទ្ធិ៖ ផ្ដល់សិទ្ធិឱ្យតែ Admin មើលឃើញផ្នែកនេះប៉ុណ្ណោះ
    user_role = st.session_state.get('role', 'user')
    if user_role != 'admin':
        return  
    
    st.markdown("### ⚡ SMC Real-time Execution & Price Monitor (Admin View)")
    st.caption("ផ្ទាំងសម្រាប់ Admin តាមដានតម្លៃទីផ្សារបច្ចុប្បន្ន និងផ្ទៀងផ្ទាត់ជាមួយ Zone ក្នុងពេលជាក់ស្តែង។")

    # Load Config បច្ចុប្បន្ន
    config = load_config()
    big_min = config.get("big_min", 3980.00)
    big_max = config.get("big_max", 4030.00)

    # ឱ្យ Admin ສາມາດបញ្ចូល ឬ Update តម្លៃ Real-time ពីទូរស័ព្ទមកផ្ទៀងផ្ទាត់បាន
    col_input1, col_input2 = st.columns([2, 1])
    with col_input1:
        live_price_input = st.number_input(
            "📊 បញ្ចូលតម្លៃ XAUUSD Real-time (ពីទូរស័ព្ទ/TradingView)", 
            value=st.session_state.get('live_price_override', 4010.915), 
            step=0.001,
            format="%.3f"
        )
        st.session_state['live_price_override'] = live_price_input

    # បង្កើត Container សម្រាប់បង្ហាញតម្លៃ Live Price និង Zone Range
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="🪙 XAUUSD Live Price", value=f"{live_price_input:,.3f}")
    
    with col2:
        st.metric(label="📍 Active Zone Range (Big Pattern)", value=f"{big_min:,.2f} - {big_max:,.2f}")

    with col3:
        # ស្ថានភាពផ្ទៀងផ្ទាត់តម្លៃជាមួយ Zone
        if big_min <= live_price_input <= big_max:
            st.success("🟢 Price is INSIDE Zone (Ready/Hit)")
        elif live_price_input > big_max:
            st.warning("📈 Price is ABOVE Zone (Premium)")
        else:
            st.info("📉 Price is BELOW Zone (Discount)")

    # ផ្នែកបង្ហាញ Sub-Patterns សម្រាប់ការតាមដានលម្អិត
    with st.expander("🔍 ดูรายละเอียด Sub-Patterns & Zone Status", expanded=True):
        sub_patterns = config.get("sub_patterns", [])
        if sub_patterns:
            for idx, sub in enumerate(sub_patterns):
                s_min = sub.get("min", 0)
                s_max = sub.get("max", 0)
                status = "🟢 HIT" if s_min <= live_price_input <= s_max else "⚪ Waiting"
                st.write(f"- **Sub-Pattern {idx+1}**: `[ {s_min:,.2f} - {s_max:,.2f} ]` — **Status**: {status}")
        else:
            st.info("ពុំទាន់มี Sub-Patterns ទេ។")
