import streamlit as st

def render_smc_manual():
    st.markdown("### 📝 SMC Manual Input Panel")
    st.caption("បញ្ចូលតម្លៃ SMC Liquidity Zones (ប្រព័ន្ធរក្សាទុក និង Update ដោយស្វ័យប្រវត្តិ)")

    # កាត់បន្ថយ Space ចន្លោះ Input
    st.markdown("""
        <style>
        .stNumberInput { margin-bottom: -8px; }
        div[data-testid="stExpander"] { margin-bottom: 6px; }
        </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 📌 1. BIG PATTERN (លំនាំចម្បង)
    # ==========================================
    st.subheader("1. Big Pattern")
    
    st.markdown("**Big Pattern Range**")
    c1, c2 = st.columns(2)
    with c1:
        st.number_input("Range Min", value=st.session_state.get('inp_bg_range_min', 4000.00), format="%.2f", key="inp_bg_range_min")
    with c2:
        st.number_input("Range Max", value=st.session_state.get('inp_bg_range_max', 4250.00), format="%.2f", key="inp_bg_range_max")

    st.markdown("**Highest Liquidity Rectangles (Supply)**")
    for i in range(1, 4):
        c1, c2 = st.columns(2)
        with c1:
            st.number_input(f"Highest Liquidity Rectangle {i} Min", value=st.session_state.get(f'inp_highest_rect_{i}_min', 4210.00 + (i * 10)), format="%.2f", key=f"inp_highest_rect_{i}_min")
        with c2:
            st.number_input(f"Highest Liquidity Rectangle {i} Max", value=st.session_state.get(f'inp_highest_rect_{i}_max', 4220.00 + (i * 10)), format="%.2f", key=f"inp_highest_rect_{i}_max")

    st.markdown("**Lowest Liquidity Rectangles (Demand)**")
    for i in range(1, 4):
        c1, c2 = st.columns(2)
        with c1:
            st.number_input(f"Lowest Liquidity Rectangle {i} Min", value=st.session_state.get(f'inp_lowest_rect_{i}_min', 4050.00 - (i * 10)), format="%.2f", key=f"inp_lowest_rect_{i}_min")
        with c2:
            st.number_input(f"Lowest Liquidity Rectangle {i} Max", value=st.session_state.get(f'inp_lowest_rect_{i}_max', 4060.00 - (i * 10)), format="%.2f", key=f"inp_lowest_rect_{i}_max")

    st.markdown("---")

    # ==========================================
    # 📌 2. 6 SUB-PATTERNS (លំនាំរងទាំង៦)
    # ==========================================
    st.subheader("2. Sub-Patterns (6 Sub-Zones)")

    for sub_idx in range(1, 7):
        with st.expander(f"🔹 Sub-Pattern {sub_idx}", expanded=(sub_idx == 1)):
            st.markdown(f"**Sub-Pattern {sub_idx} Range**")
            c1, c2 = st.columns(2)
            with c1:
                st.number_input(f"Range Min (Sub {sub_idx})", value=st.session_state.get(f'inp_sub_{sub_idx}_range_min', 4100.00), format="%.2f", key=f"inp_sub_{sub_idx}_range_min")
            with c2:
                st.number_input(f"Range Max (Sub {sub_idx})", value=st.session_state.get(f'inp_sub_{sub_idx}_range_max', 4180.00), format="%.2f", key=f"inp_sub_{sub_idx}_range_max")

            st.markdown(f"**Top Liquidity Rectangles (Sub {sub_idx})**")
            for i in range(1, 4):
                c1, c2 = st.columns(2)
                with c1:
                    st.number_input(f"Top Liquidity Rectangle {i} Min", value=st.session_state.get(f'inp_sub_{sub_idx}_top_rect_{i}_min', 4170.00 + i), format="%.2f", key=f"inp_sub_{sub_idx}_top_rect_{i}_min")
                with c2:
                    st.number_input(f"Top Liquidity Rectangle {i} Max", value=st.session_state.get(f'inp_sub_{sub_idx}_top_rect_{i}_max', 4175.00 + i), format="%.2f", key=f"inp_sub_{sub_idx}_top_rect_{i}_max")

            st.markdown(f"**Bottom Liquidity Rectangles (Sub {sub_idx})**")
            for i in range(1, 4):
                c1, c2 = st.columns(2)
                with c1:
                    st.number_input(f"Bottom Liquidity Rectangle {i} Min", value=st.session_state.get(f'inp_sub_{sub_idx}_bottom_rect_{i}_min', 4110.00 - i), format="%.2f", key=f"inp_sub_{sub_idx}_bottom_rect_{i}_min")
                with c2:
                    st.number_input(f"Bottom Liquidity Rectangle {i} Max", value=st.session_state.get(f'inp_sub_{sub_idx}_bottom_rect_{i}_max', 4115.00 - i), format="%.2f", key=f"inp_sub_{sub_idx}_bottom_rect_{i}_max")