import streamlit as st
import pandas as pd
import json
import os

CONFIG_FILE = "smc_manual_config.json"

def load_data():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return []

def save_data(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def render_smc_manual():
    st.subheader("📊 SMC Manual Input & Pattern Management")
    st.caption("បញ្ចូល និងគ្រប់គ្រងទិន្នន័យ Range និង Liquidity Zones (Top / Bottom) ព្រមទាំងធ្វើការ Merge រក A+ Pattern ស្វ័យប្រវត្តិ។")

    # យកទិន្នន័យចាស់មកបង្ហាញ
    records = load_data()

    with st.form("smc_manual_form", clear_on_submit=True):
        st.markdown("#### ✍️ បញ្ចូលទិន្នន័យថ្មី (New Range & Zones)")
        
        col_pat, col_rmin, col_rmax = st.columns([1, 1, 1])
        with col_pat:
            pattern_type = st.selectbox("Pattern Type", ["A", "B", "C"])
        with col_rmin:
            range_min = st.number_input("Range Min", value=0.000, format="%.3f")
        with col_rmax:
            range_max = st.number_input("Range Max", value=0.000, format="%.3f")

        st.markdown("---")
        st.markdown("**🔴 Liquidity Zones Top (3 Zones - Continuous Chain)**")
        t_col1, t_col2, t_col3, t_col4, t_col5, t_col6 = st.columns(6)
        with t_col1:
            t1_min = st.number_input("Top Z1 Min", value=0.000, format="%.3f")
        with t_col2:
            t1_max = st.number_input("Top Z1 Max", value=0.000, format="%.3f")
        with t_col3:
            t2_min = st.number_input("Top Z2 Min", value=0.000, format="%.3f")
        with t_col4:
            t2_max = st.number_input("Top Z2 Max", value=0.000, format="%.3f")
        with t_col5:
            t3_min = st.number_input("Top Z3 Min", value=0.000, format="%.3f")
        with t_col6:
            t3_max = st.number_input("Top Z3 Max", value=0.000, format="%.3f")

        st.markdown("**🔵 Liquidity Zones Bottom (3 Zones - Continuous Chain)**")
        b_col1, b_col2, b_col3, b_col4, b_col5, b_col6 = st.columns(6)
        with b_col1:
            b1_min = st.number_input("Bot Z1 Min", value=0.000, format="%.3f")
        with b_col2:
            b1_max = st.number_input("Bot Z1 Max", value=0.000, format="%.3f")
        with b_col3:
            b2_min = st.number_input("Bot Z2 Min", value=0.000, format="%.3f")
        with b_col4:
            b2_max = st.number_input("Bot Z2 Max", value=0.000, format="%.3f")
        with b_col5:
            b3_min = st.number_input("Bot Z3 Min", value=0.000, format="%.3f")
        with b_col6:
            b3_max = st.number_input("Bot Z3 Max", value=0.000, format="%.3f")

        submitted = st.form_submit_button("➕ រក្សាទុកទិន្នន័យ (Add Record)")
        if submitted:
            new_record = {
                "pattern": pattern_type,
                "range_min": range_min,
                "range_max": range_max,
                "top": [
                    {"min": t1_min, "max": t1_max},
                    {"min": t2_min, "max": t2_max},
                    {"min": t3_min, "max": t3_max}
                ],
                "bottom": [
                    {"min": b1_min, "max": b1_max},
                    {"min": b2_min, "max": b2_max},
                    {"min": b3_min, "max": b3_max}
                ]
            }
            records.append(new_record)
            save_data(records)
            st.success("✅ បានរក្សាទុក Range និង Zones ចូលក្នុងប្រព័ន្ធជោគជ័យ!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 បញ្ជីទិន្នន័យតារាង (SMC Records Summary)")

    if records:
        table_data = []
        all_top_maxs = []
        all_bot_mins = []

        for idx, r in enumerate(records):
            r_min = f"{r['range_min']:.3f}"
            r_max = f"{r['range_max']:.3f}"
            
            # បង្រួមបង្ហាញ Top 3 zones ឱ្យងាយមើល
            t_str = " / ".join([f"[{z['min']:.3f}-{z['max']:.3f}]" for z in r['top']])
            # បង្រួមបង្ហាញ Bottom 3 zones ឱ្យងាយមើល
            b_str = " / ".join([f"[{z['min']:.3f}-{z['max']:.3f}]" for z in r['bottom']])

            # ប្រមូលតម្លៃដើម្បីរក A+ Merge
            for z in r['top']:
                all_top_maxs.append(z['max'])
            for z in r['bottom']:
                all_bot_mins.append(z['min'] if z['min'] > 0 else 999999.0)

            table_data.append({
                "ID": idx,
                "Pattern": r['pattern'],
                "Range Zone (Min - Max)": f"{r_min} - {r_max}",
                "Liquidity Top (3 Zones)": t_str,
                "Liquidity Bottom (3 Zones)": b_str
            })

        df = pd.DataFrame(table_data)
        st.table(df.drop(columns=["ID"]))

        # 🌟 ការគណនា A+ Pattern ស្វ័យប្រវត្តិ (Auto-Merge A+)
        if all_top_maxs and all_bot_mins:
            highest_top = max(all_top_maxs)
            valid_bots = [b for b in all_bot_mins if b < 999999.0]
            lowest_bot = min(valid_bots) if valid_bots else 0.000

            st.markdown("---")
            st.info(f"✨ **Global A+ Pattern (Auto-Merged)**: Top ខ្ពស់បំផុត = **{highest_top:.3f}** | Bottom ទាបបំផុត = **{lowest_bot:.3f}**")

        st.markdown("### 🗑️ គ្រប់គ្រងទិន្នន័យ (Edit / Delete)")
        del_col1, del_col2 = st.columns([2, 1])
        with del_col1:
            selected_to_delete = st.selectbox("ជ្រើសរើសជួរ (ID) ដើម្បីលុបចេញ", options=range(len(records)), format_func=lambda x: f"Record ID {x} (Pattern: {records[x]['pattern']} | Range: {records[x]['range_min']:.3f} - {records[x]['range_max']:.3f})")
        with del_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ លុបទិន្នន័យនេះ", use_container_width=True):
                records.pop(selected_to_delete)
                save_data(records)
                st.success("🗑️ បានលុបដោយជោគជ័យ!")
                st.rerun()

        if st.button("⚠️ លុបទិន្នន័យทั้งหมด (Clear All Records)", use_container_width=True):
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            st.success("🧹 បានសម្អាតទិន្នន័យទាំងអស់រួចរាល់!")
            st.rerun()
    else:
        st.info("ℹ️ មិនទាន់មានទិន្នន័យ Range ឬ Liquidity Zones ត្រូវបានបញ្ចូលនៅឡើយទេ។ សូមបំពេញទម្រង់ខាងលើ។")
