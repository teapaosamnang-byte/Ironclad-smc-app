import streamlit as st
import feedparser
from datetime import datetime
import time

def get_gold_impact_news(limit=5):
    """
    ទាញយកព័ត៌មាន Real-Time ទើបតែចេញពី Reuters, CNN, CNBC, និង Yahoo Finance
    ហើយ Filter កាត់យកតែ ៥ ព័ត៌មានចុងក្រោយគេបង្អស់ដែលជះឥទ្ធិពលលើមាស
    """
    # ប្រភព RSS Feeds ដែលដំណើរការលឿន និងមានព័ត៌មាន Reuters ផ្ទាល់
    rss_sources = [
        # Reuters via Google News Feed (លឿន និងទាញបាន 100%)
        ("REUTERS", "https://news.google.com/rss/search?q=when:24h+site:reuters.com+gold+OR+fed+OR+dollar&ceid=US:en&hl=en-US&gl=US"),
        # CNN Money & Business Feed
        ("CNN", "http://rss.cnn.com/rss/money_news_international.rss"),
        ("CNN", "http://rss.cnn.com/rss/edition_world.rss"),
        # CNBC & Yahoo Finance សម្រាប់បន្ថែមព័ត៌មានទីផ្សារមាសលឿនៗ
        ("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
        ("YAHOO", "https://finance.yahoo.com/rss/headline?s=GC=F")
    ]
    
    # ពាក្យគន្លឹះដែលពាក់ព័ន្ធនឹងមាស/សេដ្ឋកិច្ច
    gold_keywords = [
        "gold", "xau", "fed", "federal reserve", "rate", "inflation", 
        "dollar", "usd", "cpi", "powell", "treasury", "war", "oil", 
        "economy", "central bank", "stocks", "market"
    ]
    
    all_articles = []
    
    for source_name, url in rss_sources:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.title
                title_lower = title.lower()
                
                # ពិនិត្យពាក្យគន្លឹះ
                if any(kw in title_lower for kw in gold_keywords):
                    clean_title = title.split(" - ")[0].replace('"', "'") # លុបឈ្មោះកាសែតដែលស្ទួននៅចុងចំណងជើង
                    
                    # ស្វែងរកកាលបរិច្ឆេទចេញព័ត៌មាន (Published Time)
                    pub_time = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_time = time.mktime(entry.published_parsed)
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_time = time.mktime(entry.updated_parsed)
                    else:
                        pub_time = time.time() # បើគ្មានកាលបរិច្ឆេទ យកម៉ោងបច្ចុប្បន្ន
                        
                    formatted_title = f"[{source_name}] {clean_title}"
                    
                    # ការពារកុំឱ្យស្ទួនចំណងជើង
                    if not any(a['title'] == formatted_title for a in all_articles):
                        all_articles.append({
                            'title': formatted_title,
                            'time': pub_time
                        })
        except Exception:
            continue

    # 1. តម្រៀបព័ត៌មានតាមម៉ោងចេញ (យកព័ត៌មានទើបតែចេញចុងក្រោយគេបង្អស់មកលើ)
    all_articles.sort(key=lambda x: x['time'], reverse=True)
    
    # 2. កាត់យកតែ ៥ ព័ត៌មានចុងក្រោយគេ
    latest_5 = [a['title'] for a in all_articles[:limit]]

    # ប្រសិនបើទាញពុំបាន ប្រើ Fallback ព័ត៌មានគំរូ
    if not latest_5:
        latest_5 = [
            "[REUTERS] Gold Price Reacts to US Economic Data and Dollar Movements",
            "[CNN] Federal Reserve Interest Rate Decisions Impact Global Markets",
            "[REUTERS] Geopolitical Risk Keeps Safe-Haven Demand Active for Gold",
            "[CNBC] US Dollar Index Holds Near Resistance Ahead of Key Reports",
            "[REUTERS] Traders Monitor Central Bank Activity and Inflation Metrics"
        ]

    return latest_5


def render_news_ticker():
    """បង្ហាញព័ត៌មានរត់តាមបាតអេក្រង់ដូចទូរទស្សន៍ (Marquee Ticker)"""
    news_list = get_gold_impact_news(limit=5)
    
    # ភ្ជាប់ព័ត៌មានទាំង ៥ បញ្ចូលគ្នាដោយប្រើប្រាស់និមិត្តសញ្ញា ⚡
    full_news_text = " &nbsp;&nbsp;&nbsp;&nbsp; ⚡ &nbsp;&nbsp;&nbsp;&nbsp; ".join(news_list)
    
    st.markdown(f"""
        <style>
        .news-ticker-container {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0d1117;
            color: #f0f6fc;
            padding: 8px 0;
            z-index: 99999;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.5);
            border-top: 2px solid #f59e0b;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            align-items: center;
        }}
        .news-badge {{
            background-color: #f59e0b;
            color: #000000;
            padding: 4px 12px;
            font-weight: bold;
            font-size: 12px;
            border-radius: 4px;
            margin-left: 15px;
            white-space: nowrap;
            letter-spacing: 0.5px;
        }}
        .marquee-wrapper {{
            overflow: hidden;
            white-space: nowrap;
            width: 100%;
        }}
        .marquee-content {{
            display: inline-block;
            padding-left: 100%;
            animation: marquee 30s linear infinite;
            font-size: 14px;
            font-weight: 500;
        }}
        .marquee-content:hover {{
            animation-play-state: paused;
        }}
        @keyframes marquee {{
            0%   {{ transform: translate(0, 0); }}
            100% {{ transform: translate(-100%, 0); }}
        }}
        </style>
        
        <div class="news-ticker-container">
            <div class="news-badge">🔴 BREAKING NEWS (REUTERS / CNN)</div>
            <div class="marquee-wrapper">
                <div class="marquee-content">
                    {full_news_text}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)