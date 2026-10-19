import streamlit as st
import requests
from bs4 import BeautifulSoup

def render_news_module():
    st.subheader("📰 Global Financial & Geopolitical News (Gold / War)")
    
    st.markdown("ព័ត៌មានទាន់ហេតុការណ៍ដែលប៉ះពាល់ដល់តម្លៃមាស (CNN & Reuters):")

    # ព័ត៌មានគំរូ (Mock Data / RSS Feeds អាចដាក់ជំនួសបានដើម្បីការពារ IP Blocking)
    news_items = [
        {"source": "Reuters", "title": "Gold holds near record highs as Middle East tensions escalate", "time": "15 mins ago", "url": "#"},
        {"source": "CNN", "title": "Central banks continue heavy gold buying amid global economic uncertainty", "time": "1 hour ago", "url": "#"},
        {"source": "Reuters", "title": "US Dollar dips following fresh inflation data, boosting safe-haven assets", "time": "3 hours ago", "url": "#"},
        {"source": "CNN", "title": "Geopolitical risks: How the ongoing conflicts impact bullion markets", "time": "5 hours ago", "url": "#"}
    ]

    for item in news_items:
        with st.container():
            st.markdown(f"""
                <div style="padding: 10px; margin-bottom: 8px; border-left: 3px solid #2962ff; background-color: #131722; border-radius: 4px;">
                    <span style="font-size: 12px; color: #848e9c;">{item['source']} • {item['time']}</span><br>
                    <a href="{item['url']}" target="_blank" style="color: #d1d4dc; text-decoration: none; font-weight: bold;">{item['title']}</a>
                </div>
            """, unsafe_allow_html=True)