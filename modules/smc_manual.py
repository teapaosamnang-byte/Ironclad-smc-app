import streamlit as st
import json
import os

CONFIG_FILE = "smc_manual_config.json"

def load_full_config():
    """អានទិន្នន័យសរុបទាំង system_status និង records ពី JSON"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
                elif isinstance(data, list):
                    return {"system_status": {"trading_enabled": True}, "records": data}
        except:
            pass
    return {"system_status": {"trading_enabled": True}, "records": [{
        "pattern": "A",
        "range_min": 3985.490,
        "range_max": 4030.670,
        "top": [4030.670, 4032.590, 4032.790],
        "bottom": [3985.490, 3978.180, 3975.650]
    }]}

def save_full_config(config_data):
    """រក្សាទុកទិន្នន័យសរុបចូល JSON វិញ"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

def render_smc_manual():
    st.markdown("### 🛠️ SMC Manual Zones & System Control")
    
    # ── ផ្នែកសម្រាប់គ្រប់គ្រង System Toggle (Admin Control) ──
    full_config = load_full_config()
    system_status = full_config.setdefault("system_status", {"trading_enabled": True})
    current_status = system_status.get("trading_enabled", True)
    
    st.markdown("#### ⚙️ Global Trading Switch")
    new_status = st.toggle("🟢 បើកដំណើរការប្រព័ន្ធស្វ័យប្រវត្តិ (Live Trading Enabled)", value=current_status)
    
    if new_status != current_status:
        system_status["trading_enabled"] = new_status
        save_full_config(full_config)
        if new_status:
            st.success("ប្រព័ន្ធត្រូវបាន **បើក** ឱ្យដំណើរការវិញហើយ!")
        else:
            st.warning("ប្រព័ន្ធត្រូវបាន **បិទ** (Emergency Stop) សម្រាកការចេញសញ្ញា!")
        st.rerun()
        
    st.markdown("---")
    
    records = full_config.get("records", [])
    
    if "edit_index" not in st.session_state:
        st.session_state["edit_index"] = None

    is_editing = st.session_state["edit_index"] is not None
    current_record = records[st.session_state["edit_index"]] if is_editing and records else {}

    # បែងចែក Layout ជា ២ ភាគ (Form នៅខាងឆ្វេង និង បញ្ជី Records នៅខាងស្តាំ)
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        form_title = "✏️ កែប្រែទិន្នន័យ" if is_editing else "📋 បញ្ចូលទិន្នន័យថ្មី"
        
        with st.expander(form_title, expanded=True):
            with st.form("smc_manual_form"):
                pattern_type = st.selectbox("Pattern Type", ["A", "B", "C"], index=["A", "B", "C"].index(current_record.get("pattern", "A")) if is_editing else 0)
                
                c1, c2 = st.columns(2)
                with c1:
                    range_min = st.number_input("Range Min", value=float(current_record.get("range_min", 3985.490)), format="%.3f")
                with c2:
                    range_max = st.number_input("Range Max", value=float(current_record.get("range_max", 4030.670)), format="%.3f")
                    
                st.markdown("---")
                st.markdown("🔴 **Liquidity Zones Top**")
                top_vals = current_record.get("top", [4030.670, 4032.590, 4032.790])
                t1, t2, t3 = st.columns(3)
                with t1:
                    top_z1 = st.number_input("Top Z1", value=float(top_vals[0]), format="%.3f")
                with t2:
                    top_z2 = st.number_input("Top Z2", value=float(top_vals[1]), format="%.3f")
                with t3:
                    top_z3 = st.number_input("Top Z3", value=float(top_vals[2]), format="%.3f")
                    
                st.markdown("---")
                st.markdown("🔵 **Liquidity Zones Bottom**")
                bot_vals = current_record.get("bottom", [3985.490, 3978.180, 3975.650])
                b1, b2, b3 = st.columns(3)
                with b1:
                    bot_z1 = st.number_input("Bot Z1", value=float(bot_vals[0]), format="%.3f")
                with b2:
                    bot_z2 = st.number_input("Bot Z2", value=float(bot_vals[1]), format="%.3f")
                with b3:
                    bot_z3 = st.number_input("Bot Z3", value=float(bot_vals[2]), format="%.3f")
                    
                st.write("")
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    submit_label = "💾 Update" if is_editing else "➕ Save"
                    submitted = st.form_submit_button(submit_label, use_container_width=True)
                with b_col2:
                    if is_editing:
                        cancel_clicked = st.form_submit_button("❌ Cancel", use_container_width=True)
                    else:
                        cancel_clicked = False

                if cancel_clicked:
                    st.session_state["edit_index"] = None
                    st.rerun()

                if submitted:
                    new_data = {
                        "pattern": pattern_type,
                        "range_min": range_min,
                        "range_max": range_max,
                        "top": [top_z1, top_z2, top_z3],
                        "bottom": [bot_z1, bot_z2, bot_z3]
                    }
                    
                    if is_editing:
                        records[st.session_state["edit_index"]] = new_data
                        st.session_state["edit_index"] = None
                        st.success("បានកែប្រែទិន្នន័យដោយជោគជ័យ!")
                    else:
                        records.append(new_data)
                        st.success("បានរក្សាទុកទិន្នន័យថ្មីដោយជោគជ័យ!")
                    
                    full_config["records"] = records
                    save_full_config(full_config)
                    st.rerun()

    with col_right:
        st.markdown("#### 📊 បញ្ជីទិន្នន័យ (SMC Records)")
        
        if records:
            for idx, rec in enumerate(records):
                with st.expander(f"📌 Pattern: {rec.get('pattern')} (#{idx+1})"):
                    st.caption(f"**Range:** {rec.get('range_min'):.3f} - {rec.get('range_max'):.3f}")
                    
                    top_vals = [f"{v:.3f}" for v in rec.get('top', [])]
                    bot_vals = [f"{v:.3f}" for v in rec.get('bottom', [])]
                    
                    st.markdown(f"🔴 **Top:** {', '.join(top_vals)}")
                    st.markdown(f"🔵 **Bottom:** {', '.join(bot_vals)}")
                    
                    st.write("")
                    act_c1, act_c2 = st.columns(2)
                    with act_c1:
                        if st.button("✏️ Edit", key=f"edit_btn_{idx}", use_container_width=True):
                            st.session_state["edit_index"] = idx
                            st.rerun()
                    with act_c2:
                        if st.button("🗑️ Delete", key=f"del_btn_{idx}", use_container_width=True):
                            records.pop(idx)
                            full_config["records"] = records
                            save_full_config(full_config)
                            if st.session_state["edit_index"] == idx:
                                st.session_state["edit_index"] = None
                            st.success("បានលុបទិន្នន័យ!")
                            st.rerun()
        else:
            st.info("មិនទាន់មានទិន្នន័យនៅឡើយ។")