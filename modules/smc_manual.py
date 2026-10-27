import streamlit as st
from PIL import Image
import re
import json
import os

CONFIG_FILE = "smc_config.json"

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def render_smc_manual():
    st.markdown("### 📝 SMC Manual Input & AI OCR Panel")
    st.caption("បញ្ចូលតម្លៃ SMC Liquidity Zones ដោយផ្ទាល់ ឬ Upload រូបភាព Screenshot ពី TradingView (អតិបរមា 3 រូប)")

    # គ្រប់គ្រងរូបភាព Upload តាម Session State
    if 'uploaded_vision_files' not in st.session_state:
        st.session_state['uploaded_vision_files'] = []

    uploaded_files = st.file_uploader(
        "ជ្រើសរើសរូបភាពក្រាហ្វ (PNG, JPG) - អតិបរមា 3 រូប", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True,
        key="vision_uploader_multi"
    )

    if uploaded_files:
        if len(uploaded_files) > 3:
            st.warning("⚠️ សូមជ្រើសរើសរូបភាពត្រឹមតែ 3 រូបប៉ុណ្ណោះ។")
            uploaded_files = uploaded_files[:3]
        st.session_state['uploaded_vision_files'] = uploaded_files

    # បង្ហាញរូបភាពដែលបាន Upload និងប៊ូតុងលុបចោល
    if st.session_state['uploaded_vision_files']:
        st.write(f"📁 ចំនួនរូបភាពបានបញ្ចូល: {len(st.session_state['uploaded_vision_files'])} / 3 រូប")
        
        col_prevs = st.columns(len(st.session_state['uploaded_vision_files']))
        for idx, file in enumerate(st.session_state['uploaded_vision_files']):
            with col_prevs[idx]:
                st.image(file, width=120, caption=f"រូបទី {idx+1}")

        if st.button("🗑️ លុបរូបភាពទាំងអស់ចេញ (Clear Images)", use_container_width=True):
            st.session_state['uploaded_vision_files'] = []
            st.rerun()

    st.markdown("---")

    # ==========================================
    # 📌 1. BIG PATTERNS (អាចបញ្ចូល Big Pattern បាន 3)
    # ==========================================
    st.subheader("1. Big Patterns (អាចកំណត់បាន 3)")
    
    for bp in range(1, 4):
        with st.expander(f"📌 Big Pattern {bp}", expanded=(bp == 1)):
            c1, c2 = st.columns(2)
            with c1:
                st.number_input(f"Big Pattern {bp} Min", value=float(st.session_state.get(f'inp_bg_{bp}_min', 4000.00 + (bp*10))), format="%.2f", key=f"inp_bg_{bp}_min")
            with c2:
                st.number_input(f"Big Pattern {bp} Max", value=float(st.session_state.get(f'inp_bg_{bp}_max', 4050.00 + (bp*10))), format="%.2f", key=f"inp_bg_{bp}_max")

            st.markdown(f"**Highest Liquidity Rectangles (Supply - Big {bp})**")
            for i in range(1, 4):
                c1, c2 = st.columns(2)
                with c1:
                    st.number_input(f"High Rect {i} Min", value=float(st.session_state.get(f'inp_bg_{bp}_highest_{i}_min', 4210.00)), format="%.2f", key=f"inp_bg_{bp}_highest_{i}_min")
                with c2:
                    st.number_input(f"High Rect {i} Max", value=float(st.session_state.get(f'inp_bg_{bp}_highest_{i}_max', 4220.00)), format="%.2f", key=f"inp_bg_{bp}_highest_{i}_max")

            st.markdown(f"**Lowest Liquidity Rectangles (Demand - Big {bp})**")
            for i in range(1, 4):
                c1, c2 = st.columns(2)
                with c1:
                    st.number_input(f"Low Rect {i} Min", value=float(st.session_state.get(f'inp_bg_{bp}_lowest_{i}_min', 3980.00)), format="%.2f", key=f"inp_bg_{bp}_lowest_{i}_min")
                with c2:
                    st.number_input(f"Low Rect {i} Max", value=float(st.session_state.get(f'inp_bg_{bp}_lowest_{i}_max', 3990.00)), format="%.2f", key=f"inp_bg_{bp}_lowest_{i}_max")

    st.markdown("---")

    # ==========================================
    # 📌 2. SUB-PATTERNS (ដាក់ក្នុង Expander កុំឱ្យវែងពេក)
    # ==========================================
    st.subheader("2. Sub-Patterns (6 Sub-Zones)")

    for sub_idx in range(1, 7):
        with st.expander(f"🔹 Sub-Pattern {sub_idx} (ចុចដើម្បីបើកดู)", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.number_input(f"Range Min (Sub {sub_idx})", value=float(st.session_state.get(f'inp_sub_{sub_idx}_range_min', 4100.00)), format="%.2f", key=f"inp_sub_{sub_idx}_range_min")
            with c2:
                st.number_input(f"Range Max (Sub {sub_idx})", value=float(st.session_state.get(f'inp_sub_{sub_idx}_range_max', 4180.00)), format="%.2f", key=f"inp_sub_{sub_idx}_range_max")

            st.markdown(f"**Top Liquidity Rectangles (Sub {sub_idx})**")
            for i in range(1, 4):
                c1, c2 = st.columns(2)
                with c1:
                    st.number_input(f"Top Rect {i} Min", value=float(st.session_state.get(f'inp_sub_{sub_idx}_top_rect_{i}_min', 4170.00)), format="%.2f", key=f"inp_sub_{sub_idx}_top_rect_{i}_min")
                with c2:
                    st.number_input(f"Top Rect {i} Max", value=float(st.session_state.get(f'inp_sub_{sub_idx}_top_rect_{i}_max', 4175.00)), format="%.2f", key=f"inp_sub_{sub_idx}_top_rect_{i}_max")

            st.markdown(f"**Bottom Liquidity Rectangles (Sub {sub_idx})**")
            for i in range(1, 4):
                c1, c2 = st.columns(2)
                with c1:
                    st.number_input(f"Bottom Rect {i} Min", value=float(st.session_state.get(f'inp_sub_{sub_idx}_bottom_rect_{i}_min', 4110.00)), format="%.2f", key=f"inp_sub_{sub_idx}_bottom_rect_{i}_min")
                with c2:
                    st.number_input(f"Bottom Rect {i} Max", value=float(st.session_state.get(f'inp_sub_{sub_idx}_bottom_rect_{i}_max', 4115.00)), format="%.2f", key=f"inp_sub_{sub_idx}_bottom_rect_{i}_max")
