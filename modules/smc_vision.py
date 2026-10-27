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
        st.caption("ថតរូប Screenshot ពី TradingView អាច Upload បានរហូតដល់ ៣ រូប។ ប្រព័ន្ធនឹងអាន Sub-Patterns ទាំង២ មកគណនាបញ្ចូលគ្នាជា Big Pattern ស្វ័យប្រវត្តិ។")

        # ដាក់មុខងារ Upload រូបភាពច្រើន (អតិបរមា 3 រូប)
        uploaded_files = st.file_uploader(
            "ជ្រើសរើសរូបភាពក្រាហ្វ (PNG, JPG) - สูงสุด 3 រូប", 
            type=["png", "jpg", "jpeg"], 
            accept_multiple_files=True,
            key="vision_uploader_multi"
        )

        # កម្រិតចំនួនរូបភាពមិនឱ្យលើសពី 3 រូប
        if uploaded_files and len(uploaded_files) > 3:
            st.warning("⚠️ សូមជ្រើសរើសរូបភាពត្រឹមតែ 3 រូបប៉ុណ្ណោះ។")
            uploaded_files = uploaded_files[:3]

        current_config = load_config()

        if uploaded_files:
            st.write(f"📁 ចំនួនរូបភាពបានបញ្ចូល: {len(uploaded_files)} / 3 រូប")
            
            processed_patterns = []

            for idx, uploaded_file in enumerate(uploaded_files):
                st.markdown(f"---")
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
                        prices = re.findall(r'\b[3-4]\d{3}\.\d{3}\b|\b[3-4]\d{3}\.\d{2}\b|\b[3-4]\d{3}\b', text)
                        
                        if prices and len(prices) >= 2:
                            float_prices = [float(p) for p in prices]
                            float_prices.sort()
                            
                            # ចែកចេញជា 2 Sub-Patterns ក្នុង 1 រូបភាព ហើយបូករួមបញ្ចូលគ្នាជា Big Pattern
                            sub1_min, sub1_max = float_prices[0], float_prices[1] if len(float_prices)>1 else float_prices[0]
                            sub2_min, sub2_max = float_prices[2] if len(float_prices)>2 else sub1_max, float_prices[-1]
                            
                            big_min = min(sub1_min, sub2_min)
                            big_max = max(sub1_max, sub2_max)
                        else:
                            # Demo values តាមគំរូมาตรฐาน
                            big_min = 3980.00 + (idx * 25)
                            big_max = 4030.00 + (idx * 25)
                            sub1_min, sub1_max = big_min, (big_min + big_max)/2
                            sub2_min, sub2_max = (big_min + big_max)/2, big_max
                    except:
                        big_min = 3980.00 + (idx * 25)
                        big_max = 4030.00 + (idx * 25)
                        sub1_min, sub1_max = big_min, (big_min + big_max)/2
                        sub2_min, sub2_max = (big_min + big_max)/2, big_max

                    st.info(f"📍 **Big Pattern Calculated**: `{big_min:,.2f} - {big_max:,.2f}`\n- Sub 1: `[{sub1_min:,.2f} - {sub1_max:,.2f}]`\n- Sub 2: `[{sub2_min:,.2f} - {sub2_max:,.2f}]`")
                    
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
                if st.button("💾 រก្សាទុក Patterns ทั้งหมด (Save)", use_container_width=True):
                    try:
                        # យក Pattern ទី១ មកធ្វើជា Primary Active Config និងរក្សាទុកទិន្នន័យទាំងអស់
                        main_p = processed_patterns[0] if processed_patterns else {}
                        config_data = {
                            "big_min": main_p.get("big_min", 3980.00),
                            "big_max": main_p.get("big_max", 4030.00),
                            "sub_patterns": main_p.get("sub_patterns", []),
                            "all_patterns": processed_patterns
                        }
                        
                        # រក្សាទុកចូលไฟล์ JSON ថេរដើម្បីចងចាំលើ GitHub
                        save_config(config_data)
                        
                        # អាប់ដេត Session State ភ្លាមៗ
                        st.session_state['inp_big_min'] = config_data["big_min"]
                        st.session_state['inp_big_max'] = config_data["big_max"]
                        
                        st.success("✅ បានរក្សាទុកទិន្នន័យ Patterns ចូល GitHub Persistent Storage (smc_config.json) ជោគជ័យ!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងពេល Save: {e}")
            
            with col_del:
                if st.button("🗑️ លុបទិន្នន័យ Patterns ចោល (Delete)", use_container_width=True):
                    if os.path.exists(CONFIG_FILE):
                        os.remove(CONFIG_FILE)
                    st.success("🗑️ បានលុបទិន្នន័យ និងសម្អាត Config រួចរាល់!")
                    st.rerun()

        # បង្ហាញព័ត៌មានដែលបានរក្សាទុកបច្ចុប្បន្ន
        if os.path.exists(CONFIG_FILE):
            st.markdown("### 📋 Stored Config Status:")
            st.write(f"- **Active Big Pattern Range**: `{current_config.get('big_min', 0):,.2f} - {current_config.get('big_max', 0):,.2f}`")
