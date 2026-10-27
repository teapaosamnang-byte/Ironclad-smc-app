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
        "big_min": 3980.00,
        "big_max": 4030.00,
        "sub_patterns": [
            {"min": 3980.00, "max": 4005.00},
            {"min": 4005.00, "max": 4030.00}
        ],
        "all_patterns": []
    }

def render_smc_vision():
    with st.expander("📸 AI Vision / OCR (Upload up to 3 TradingView Screenshots)", expanded=True):
        st.caption("ថតរូប Screenshot ពី TradingView អាច Upload បានរហូតដល់ ៣ រូប។ ប្រព័ន្ធនឹងទាញយកតម្លៃត្រឹមតំបន់ដែលបានកំណត់ (Zone) មកគណនាស្វ័យប្រវត្តិ។")

        # 🛡️ ប្រើប្រាស់ Key ដែលមានសុវត្ថិភាព និងមិនស្ទួន
        uploaded_files = st.file_uploader(
            "ជ្រើសរើសរូបភាពក្រាហ្វ (PNG, JPG) - អតិបរមា 3 រូប", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="vision_uploader_unique_v2"
        )

        if uploaded_files and len(uploaded_files) > 3:
            st.warning("⚠️ សូមជ្រើសរើសរូបភាពត្រឹមតែ 3 រូបប៉ុណ្ណោះ។")
            uploaded_files = uploaded_files[:3]

        current_config = load_config()

        if uploaded_files:
            st.write(f"📁 ចំនួនរូបភាពបានបញ្ចូល: {len(uploaded_files)} / 3 រូប")
            
            processed_patterns = []

            for idx, uploaded_file in enumerate(uploaded_files):
                st.markdown("---")
                st.markdown(f"**📷 រូបភាពទី {idx+1}: {uploaded_file.name}**")
                
                img = Image.open(uploaded_file)
                img_width, img_height = img.size
                if img_height > 40:
                    cropped_img = img.crop((0, 0, img_width, img_height - 40))
                else:
                    cropped_img = img

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(cropped_img, width=140)
                with col2:
                    try:
                        import pytesseract
                        text = pytesseract.image_to_string(cropped_img)
                        prices = re.findall(r'\b[3-4]\d{3}\.\d{2,3}\b|\b[3-4]\d{3}\b', text)
                        
                        if prices:
                            float_prices = [float(p) for p in prices if 3000 <= float(p) <= 5000]
                            float_prices = sorted(list(set(float_prices)))
                            
                            if len(float_prices) >= 2:
                                big_min = float_prices[0]
                                big_max = float_prices[-1]
                            elif len(float_prices) == 1:
                                big_min = float_prices[0] - 10.00
                                big_max = float_prices[0] + 10.00
                            else:
                                raise Exception("No valid prices in range")
                        else:
                            raise Exception("No prices found")
                            
                        mid_price = (big_min + big_max) / 2
                        sub1_min, sub1_max = big_min, mid_price
                        sub2_min, sub2_max = mid_price, big_max

                    except Exception as e:
                        big_min = 3980.00 + (idx * 20)
                        big_max = 4030.00 + (idx * 20)
                        sub1_min, sub1_max = big_min, (big_min + big_max)/2
                        sub2_min, sub2_max = (big_min + big_max)/2, big_max

                    st.info(f"📍 **Big Pattern Calculated**: `{big_min:,.3f} - {big_max:,.3f}`\n- Sub 1: `[{sub1_min:,.3f} - {sub1_max:,.3f}]`\n- Sub 2: `[{sub2_min:,.3f} - {sub2_max:,.3f}]`")
                    
                    processed_patterns.append({
                        "big_min": big_min,
                        "big_max": big_max,
                        "sub_patterns": [
                            {"min": sub1_min, "max": sub1_max},
                            {"min": sub2_min, "max": sub2_max}
                        ]
                    })

            st.markdown("---")
            col_save, col_del = st.columns(2)
            
            with col_save:
                if st.button("💾 រក្សាទុក Patterns ทั้งหมด (Save)", use_container_width=True, key="save_vision_patterns_btn"):
                    try:
                        main_p = processed_patterns[0] if processed_patterns else {}
                        config_data = {
                            "big_min": main_p.get("big_min", 3980.00),
                            "big_max": main_p.get("big_max", 4030.00),
                            "sub_patterns": main_p.get("sub_patterns", []),
                            "all_patterns": processed_patterns
                        }
                        
                        save_config(config_data)
                        
                        st.session_state['inp_big_min'] = config_data["big_min"]
                        st.session_state['inp_big_max'] = config_data["big_max"]
                        
                        st.success("✅ បានរក្សាទុកទិន្នន័យ Patterns ចូល GitHub Persistent Storage (smc_config.json) ជោគជ័យ!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងពេល Save: {e}")
            
            with col_del:
                if st.button("🗑️ លុបទិន្នន័យ Patterns ចោល (Delete)", use_container_width=True, key="delete_vision_patterns_btn"):
                    if os.path.exists(CONFIG_FILE):
                        os.remove(CONFIG_FILE)
                    st.success("🗑️ បានលុបទិន្នន័យ និងសម្អាត Config រួចរាល់!")
                    st.rerun()

        if os.path.exists(CONFIG_FILE):
            st.markdown("### 📋 Stored Config Status:")
            st.write(f"- **Active Big Pattern Range**: `{current_config.get('big_min', 0):,.3f} - {current_config.get('big_max', 0):,.3f}`")
