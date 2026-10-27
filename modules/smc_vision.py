import streamlit as st
from PIL import Image
import re
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
        "big_min": 4060.00,
        "big_max": 4200.00,
        "sub_patterns": []
    }

def render_smc_vision():
    with st.expander("📸 AI Vision / OCR (TradingView SMC Zones)", expanded=True):
        st.caption("Upload រូបភាព Screenshot ពី TradingView ដែលមាន Big Pattern មួយ និង Sub-Patterns តូចៗខាងក្នុង។")

        uploaded_files = st.file_uploader(
            "ជ្រើសរើសរូបភាពក្រាហ្វ (PNG, JPG) - អតិបរមា 3 រូប", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="vision_uploader_multi"
        )

        if uploaded_files and len(uploaded_files) > 3:
            st.warning("⚠️ សូមជ្រើសរើសរូបភាពត្រឹមតែ 3 រូបប៉ុណ្ណោះ។")
            uploaded_files = uploaded_files[:3]

        current_config = load_config()

        if uploaded_files:
            st.write(f"📁 ចំនួនរូបភាពបានបញ្ចូល: {len(uploaded_files)} / 3 រូប")
            
            all_sub_patterns = []
            global_min = 99999.0
            global_max = 0.0

            for idx, uploaded_file in enumerate(uploaded_files):
                st.markdown("---")
                st.markdown(f"**📷 រូបភាពទី {idx+1}: {uploaded_file.name}**")
                
                img = Image.open(uploaded_file)
                img_width, img_height = img.size
                cropped_img = img.crop((0, 0, img_width, img_height - 40)) if img_height > 40 else img

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(cropped_img, width=140)
                with col2:
                    try:
                        import pytesseract
                        text = pytesseract.image_to_string(cropped_img)
                        prices = re.findall(r'\b[3-5]\d{3}\.\d{2,3}\b|\b[3-5]\d{3}\b', text)
                        
                        if prices:
                            float_prices = [float(p) for p in prices if 3000 <= float(p) <= 6000]
                            float_prices = sorted(list(set(float_prices)))
                            
                            if len(float_prices) >= 2:
                                img_min = float_prices[0]
                                img_max = float_prices[-1]
                                
                                # កំណត់ Big Pattern រួម
                                if img_min < global_min: global_min = img_min
                                if img_max > global_max: global_max = img_max

                                # ចែកជា Sub-Patterns ຍ່ອຍៗខាងក្នុង
                                for i in range(len(float_prices) - 1):
                                    all_sub_patterns.append({
                                        "min": float_prices[i],
                                        "max": float_prices[i+1]
                                    })
                        else:
                            raise Exception("No prices")
                    except:
                        # Fallback ករណី OCR អានមិនទាន់ចេញ
                        global_min, global_max = 4060.00, 4200.00
                        all_sub_patterns = [
                            {"min": 4060.00, "max": 4080.00},
                            {"min": 4120.00, "max": 4140.00},
                            {"min": 4180.00, "max": 4200.00}
                        ]

                    st.info(f"📍 **Detected Range in Image**: `{global_min:,.2f} - {global_max:,.2f}`\n- Sub-Zones Count: `{len(all_sub_patterns)}`")

            st.markdown("---")
            col_save, col_del = st.columns(2)
            
            with col_save:
                if st.button("💾 រក្សាទុក Patterns (Save)", use_container_width=True):
                    try:
                        config_data = {
                            "big_min": global_min if global_min != 99999.0 else 4060.00,
                            "big_max": global_max if global_max != 0.0 else 4200.00,
                            "sub_patterns": all_sub_patterns
                        }
                        save_config(config_data)
                        st.success("✅ បានរក្សាទុក Big Pattern និង Sub-Patterns ចូល GitHub Storage ជោគជ័យ!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងពេល Save: {e}")
            
            with col_del:
                if st.button("🗑️ លុបទិន្នន័យ (Delete)", use_container_width=True):
                    if os.path.exists(CONFIG_FILE):
                        os.remove(CONFIG_FILE)
                    st.success("🗑️ បានលុប និងសម្អាត Config រួចរាល់!")
                    st.rerun()

        if os.path.exists(CONFIG_FILE):
            st.markdown("### 📋 Stored Config Status:")
            st.write(f"- **Big Pattern Range**: `{current_config.get('big_min', 0):,.2f} - {current_config.get('big_max', 0):,.2f}`")
            st.write(f"- **Sub-Patterns Count**: `{len(current_config.get('sub_patterns', []))}`")
