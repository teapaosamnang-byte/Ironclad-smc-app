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
    # Default Config structure for Big Pattern & Sub-Patterns
    return {
        "big_min": 3980.00,
        "big_max": 4030.00,
        "sub_patterns": [
            {"min": 3990.00, "max": 4010.00},
            {"min": 4010.00, "max": 4025.00}
        ]
    }

def render_smc_vision():
    with st.expander("📸 AI Vision / OCR (Upload TradingView Screenshot)", expanded=True):
        st.caption("ថតរូប Screenshot ពី TradingView Upload ទីនេះ ដើម្បីឱ្យប្រព័ន្ធអានតម្លៃ និងកំណត់ចូល Big Pattern & Sub-Patterns ដោយស្វ័យប្រវត្តិ។")

        uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាពក្រាហ្វ (PNG, JPG)", type=["png", "jpg", "jpeg"], key="vision_uploader")

        current_config = load_config()

        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            
            # កាត់ផ្នែកខាងក្រោមចេញប្រហែល 40 pixels เพื่อซ่อนคำว่า Bear...
            img_width, img_height = img.size
            if img_height > 40:
                cropped_img = img.crop((0, 0, img_width, img_height - 40))
            else:
                cropped_img = img

            # ដាក់រូបភាពចំកណ្តាលជាមួយទំហំតូចសមរម្យសម្រាប់ទូរស័ព្ទ
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(cropped_img, width=180)

            if st.button("🔍 ស្កេនតម្លៃស្វ័យប្រវត្តិ (Run OCR Vision)", use_container_width=True):
                with st.spinner("⏳ កំពុងវិភាគរូបភាព និងទាញយកកម្រិតតម្លៃ SMC Patterns..."):
                    try:
                        import pytesseract
                        text = pytesseract.image_to_string(cropped_img)
                        prices = re.findall(r'\b[3-4]\d{3}\.\d{2}\b|\b[3-4]\d{3}\b', text)
                        
                        if prices and len(prices) >= 2:
                            # បម្លែងតម្លៃដែលស្កេនបានមកដាក់ជា float
                            float_prices = [float(p) for p in prices]
                            float_prices.sort(reverse=True) # រៀបពីធំទៅតូច
                            
                            st.session_state['ocr_big_max'] = float_prices[0]
                            st.session_state['ocr_big_min'] = float_prices[-1]
                            st.success(f"✅ បានរកឃើញតម្លៃ Big Pattern៖ Min={st.session_state['ocr_big_min']}, Max={st.session_state['ocr_big_max']}")
                        else:
                            # Demo fallback values ប្រសិនបើ OCR មិនទាន់ចាប់បានអត្ថបទច្បាស់លាស់
                            st.session_state['ocr_big_min'] = 3980.00
                            st.session_state['ocr_big_max'] = 4030.00
                            st.success("✅ [Demo] បានទាញយកតម្លៃ Sample សម្រាប់ Big Pattern & Sub-Patterns!")

                    except Exception as e:
                        st.info("💡 កំពុងប្រើប្រាស់ Simulation Mode សម្រាប់ OCR ។")
                        st.session_state['ocr_big_min'] = 3980.00
                        st.session_state['ocr_big_max'] = 4030.00
                        st.success("✅ បានទាញយកតម្លៃ Sample រួចរាល់!")

            # ប៊ូតុង Save សម្រាប់រក្សាទុកតម្លៃ OCR ចូល File ថេរ និង Session State របស់ Manual Input Panel
            if 'ocr_big_min' in st.session_state:
                st.markdown("---")
                st.info(f"📋 តម្លៃត្រៀមរក្សាទុក: Big Min={st.session_state['ocr_big_min']}, Big Max={st.session_state['ocr_big_max']}")
                
                if st.button("💾 រក្សាទុកតម្លៃចូល SMC Manual Panel (Save)", use_container_width=True):
                    try:
                        new_data = {
                            "big_min": st.session_state['ocr_big_min'],
                            "big_max": st.session_state['ocr_big_max'],
                            "sub_patterns": [
                                {"min": st.session_state['ocr_big_min'], "max": (st.session_state['ocr_big_min'] + st.session_state['ocr_big_max'])/2},
                                {"min": (st.session_state['ocr_big_min'] + st.session_state['ocr_big_max'])/2, "max": st.session_state['ocr_big_max']}
                            ]
                        }
                        # រក្សាទុកចូលไฟล์ JSON ថេរ
                        save_config(new_data)
                        
                        # អាប់ដេតចូល Session State ផ្ទាល់ដើម្បីឱ្យ Manual Input Panel ទទួលយកភ្លាមៗ
                        st.session_state['inp_big_min'] = new_data["big_min"]
                        st.session_state['inp_big_max'] = new_data["big_max"]
                        
                        st.success("✅ បានរក្សាទុក និងអាប់ដេតតម្លៃចូល Big Pattern & Sub-Patterns ជោគជ័យ!")
                        
                        # សម្អាត Temp State
                        del st.session_state['ocr_big_min']
                        del st.session_state['ocr_big_max']
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងពេល Save: {e}")
        
        # Load ค่าเดิมเข้าสู่ Session State ពេលបើក App លើកដំបូង
        if 'inp_big_min' not in st.session_state:
            st.session_state['inp_big_min'] = current_config.get("big_min", 3980.00)
        if 'inp_big_max' not in st.session_state:
            st.session_state['inp_big_max'] = current_config.get("big_max", 4030.00)
