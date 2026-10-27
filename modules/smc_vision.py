import streamlit as st
from PIL import Image
import re

def render_smc_vision():
    with st.expander("📸 AI Vision / OCR (Upload TradingView Screenshot)", expanded=False):
        st.caption("ថតរូប Screenshot ពី TradingView ដែលបានគូស Zones រួច Upload ទីនេះ ដើម្បីឱ្យប្រព័ន្ធអានតម្លៃបញ្ចូលដោយស្វ័យប្រវត្តិ។")

        uploaded_file = st.file_uploader("ជ្រើសរើសរូបភាពក្រាហ្វ (PNG, JPG)", type=["png", "jpg", "jpeg"], key="vision_uploader")

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded TradingView Chart", use_container_width=True)

            if st.button("🔍 ស្កេនតម្លៃស្វ័យប្រវត្តិ (Run OCR Vision)", use_container_width=True):
                with st.spinner("⏳ កំពុងវិភាគរូបភាព និងទាញយកកម្រិតតម្លៃ SMC Zones..."):
                    try:
                        import pytesseract
                        text = pytesseract.image_to_string(image)
                        prices = re.findall(r'\b[3-4]\d{3}\.\d{2}\b|\b[3-4]\d{3}\b', text)
                        
                        if prices:
                            st.session_state['temp_ocr_prices'] = prices
                            st.success(f"✅ បានរកឃើញតម្លៃ៖ {', '.join(prices[:6])}")
                        else:
                            st.warning("⚠️ រកមិនឃើញកម្រិតតម្លៃច្បាស់លាស់ពី OCR ។")

                    except ImportError:
                        st.info("💡 ប្រព័ន្ធ OCR កំពុងស្ថិតក្នុងទម្រង់ Simulation ។")
                        st.session_state['temp_ocr_prices'] = ["4250.00", "4050.00"]
                        st.success("✅ [Demo] បានទាញយកតម្លៃ Sample រួចរាល់!")
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងក្នុងការអានរូបភាព: {e}")

            # ប៊ូតុង Save សម្រាប់រក្សាទុកតម្លៃ OCR ចូលប្រព័ន្ធជាក់ស្តែង
            if 'temp_ocr_prices' in st.session_state and st.session_state['temp_ocr_prices']:
                st.markdown("---")
                st.info(f"📋 តម្លៃដែលទាញបានត្រៀមរក្សាទុក៖ {st.session_state['temp_ocr_prices'][:4]}...")
                if st.button("💾 រក្សាទុកតម្លៃ OCR (Save OCR Data)", use_container_width=True):
                    try:
                        prices = st.session_state['temp_ocr_prices']
                        st.session_state['inp_bg_range_min'] = float(prices[-1])
                        st.session_state['inp_bg_range_max'] = float(prices[0])
                        st.success("✅ បានរក្សាទុក និងអាប់ដេតតម្លៃ SMC Zones ចូលប្រព័ន្ធដោយជោគជ័យ!")
                        del st.session_state['temp_ocr_prices']
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ កំហុសឆ្គងពេល Save: {e}")
