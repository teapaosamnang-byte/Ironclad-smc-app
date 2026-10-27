import streamlit as st
from PIL import Image
import re
import json
import os

CONFIG_FILE = "smc_config.json"

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"bg_min": 4000.00, "bg_max": 4250.00}

def render_smc_vision():
    with st.expander("📸 AI Vision / OCR (Upload TradingView Screenshot)", expanded=False):
        st.caption("ថតរូប Screenshot ពី TradingView Upload ទីនេះ ដើម្បីឱ្យប្រព័ន្ធអានតម្លៃបញ្ចូលដោយស្វ័យប្រវត្តិ។")

        uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាពក្រាហ្វ (PNG, JPG)", type=["png", "jpg", "jpeg"], key="vision_uploader")

        current_config = load_config()

        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            
            # កាត់ផ្នែកខាងក្រោមចេញ (កាត់ចោលប្រហែល 40 pixels ដើម្បីបំបាត់អក្សរ Bear...)
            img_width, img_height = img.size
            if img_height > 40:
                cropped_img = img.crop((0, 0, img_width, img_height - 40))
            else:
                cropped_img = img

            # ដាក់រូបភាពให้อยู่ចំកណ្តាល និងកំណត់ទំហំឱ្យតូចល្មមសមរម្យលើទូរស័ព្ទ
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(cropped_img, width=180)

            if st.button("🔍 ស្កេនតម្លៃស្វ័យប្រវត្តិ (Run OCR Vision)", use_container_width=True):
                with st.spinner("⏳ កំពុងវិភាគរូបភាព និងទាញយកកម្រិតតម្លៃ SMC Zones..."):
                    try:
                        import pytesseract
                        text = pytesseract.image_to_string(cropped_img)
                        prices = re.findall(r'\b[3-4]\d{3}\.\d{2}\b|\b[3-4]\d{3}\b', text)
                        
                        if prices:
                            st.session_state['temp_ocr_min'] = float(prices[-1])
                            st.session_state['temp_ocr_max'] = float(prices[0])
                            st.success(f"✅ បានរកឃើញតម្លៃ៖ {', '.join(prices[:6])}")
                        else:
                            st.warning("⚠️ រកមិនឃើញកម្រិតតម្លៃច្បាស់លាស់ពី OCR ។")

                    except ImportError:
                        st.info("💡 ប្រព័ន្ធ OCR កំពុងស្ថិតក្នុងទម្រង់ Simulation ។")
                        st.session_state['temp_ocr_min'] = 4050.00
                        st.session_state['temp_ocr_max'] = 4250.00
                        st.success("✅ [Demo] បានទាញយកតម្លៃ Sample រួចរាល់!")
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងក្នុងការអានរូបភាព: {e}")

            if 'temp_ocr_min' in st.session_state:
                st.markdown("---")
                st.info(f"📋 តម្លៃត្រៀមរក្សាទុក: Min={st.session_state['temp_ocr_min']}, Max={st.session_state['temp_ocr_max']}")
                if st.button("💾 រក្សាទុកតម្លៃ OCR (Save OCR Data)", use_container_width=True):
                    try:
                        new_data = {
                            "bg_min": st.session_state['temp_ocr_min'],
                            "bg_max": st.session_state['temp_ocr_max']
                        }
                        save_config(new_data)
                        
                        st.session_state['inp_bg_range_min'] = new_data["bg_min"]
                        st.session_state['inp_bg_range_max'] = new_data["bg_max"]
                        
                        st.success("✅ បានរក្សាទុក និងអាប់ដេតតម្លៃ SMC Zones ចូល File ថេរដោយជោគជ័យ!")
                        del st.session_state['temp_ocr_min']
                        del st.session_state['temp_ocr_max']
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងពេល Save: {e}")
        
        if 'inp_bg_range_min' not in st.session_state:
            st.session_state['inp_bg_range_min'] = current_config["bg_min"]
        if 'inp_bg_range_max' not in st.session_state:
            st.session_state['inp_bg_range_max'] = current_config["bg_max"]
