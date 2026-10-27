import streamlit as st
from modules.smc_analysis import analyze_advanced_smc_setup

def render_smc_execution():
    st.subheader("⚡ SMC Execution Dashboard & Institutional Alerts")

    # ហៅដំណើរការវិភាគ
    results = analyze_advanced_smc_setup()
    
    # ----------------------------------------------------
    # 🚨 1. NEWS BOX & STAND ASIDE WARNING (4H BASE BUILDING)
    # ----------------------------------------------------
    if results["stand_aside"]:
        if results["base_building"]:
            st.warning("""
                ⚠️ **4H MARKET STRUCTURE ADVISORY (BASE BUILDING PHASE):**  
                * **ស្ថានភាពទីផ្សារ៖** តម្លៃមាស (XAUUSD) លើ Timeframe 4H កំពុងស្ថិតក្នុងដំណាក់កាលសាងសង់មូលដ្ឋានតម្លៃ (Base Building / Consolidation)។  
                * **ការណែនាំ៖** **Stand Aside (រង់ចាំមើលអសកម្ម)** ជាដាច់ខាត។ សញ្ញា Entry ទាំងអស់ត្រូវបាន **លាក់/បញ្ឈប់ការបង្ហាញ** ព្រោះហានិភ័យខ្ពស់ខ្លាំង។  
                * **សកម្មភាពបន្ទាប់៖** សូមរង់ចាំរហូតទាល់តែតម្លៃចេញផុតពីតំបន់នេះ ឬ **ទម្លាក់រូបភាព Screenshot 4H ថ្មី** ចូលមកក្នុងប្រព័ន្ធ ដើម្បីវិភាគជាថ្មី!
            """)
        elif results["fakeout_trap"]:
            st.error(f"🚨 **HIGH-RISK TRAP ZONE ALERT:** រកឃើញសញ្ញា Fakeout ក្នុង Range `{results['trap_range']}`។ Entry ត្រូវបានផ្អាកទាំងស្រុង!")
        elif results["macro_bo_failed"]:
            st.error("🚨 **MACRO BREAKOUT FAILURE:** តម្លៃทำ False Breakout។ ផ្អាកការបង្ហាញ Entry ទាំងស្រុង!")

    st.markdown("---")

    # ----------------------------------------------------
    # 📊 2. ACTIVE EXECUTION SETUPS (Hidden when Base Building)
    # ----------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟢 A+ Buy Setup")
        buy = results["buy_setup"]
        if buy:
            st.info(f"**Action:** {buy['action']}\n\n"
                    f"* **Entry Price:** `{buy['entry']}`\n"
                    f"* **Stop Loss (SL):** `{buy['sl']}`\n"
                    f"* **Take Profit (TP):** `{buy['tp']}`\n"
                    f"* **Risk/Reward Ratio:** `1 : {buy['risk_reward']}`")
        else:
            st.markdown("❌ *គ្មានសញ្ញា Buy Active ទេ (មាសកំពុងសាង Base លើ 4H ត្រូវរង់ចាំ Screenshot ថ្មី)*")

    with col2:
        st.markdown("### 🔴 A+ Sell Setup")
        sell = results["sell_setup"]
        if sell:
            st.warning(f"**Action:** {sell['action']}\n\n"
                       f"* **Entry Price:** `{sell['entry']}`\n"
                       f"* **Stop Loss (SL):** `{sell['sl']}`\n"
                       f"* **Take Profit (TP):** `{sell['tp']}`\n"
                       f"* **Risk/Reward Ratio:** `1 : {sell['risk_reward']}`")
        else:
            st.markdown("❌ *គ្មានសញ្ញា Sell Active ទេ (មាសកំពុងសាង Base លើ 4H ត្រូវរង់ចាំ Screenshot ថ្មី)*")