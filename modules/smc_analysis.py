import streamlit as st
import yfinance as yf
import pandas as pd

def fetch_realtime_gold_data():
    """
    ទាញយកទិន្នន័យ Live Price និង Candlestick 5m / 15m របស់ XAUUSD (Gold) ក្នុងពេលជាក់ស្តែង
    """
    try:
        # ទាញយកទិន្នន័យ 5m ពី yfinance (GC=F ជា Gold Futures ឬ XAUUSD=X)
        ticker = yf.Ticker("GC=F")
        df_5m = ticker.history(period="1d", interval="5m")
        df_15m = ticker.history(period="1d", interval="15m")
        
        if not df_5m.empty and not df_15m.empty:
            current_price = round(df_5m['Close'].iloc[-1], 2)
            
            # ទាញយក Candlestick 5m ទី ២ នៃ 15m ដើម
            # 1 ទៀន 15m = 3 ទៀន 5m ( index -1, -2, -3 ) -> ទៀនទី 2 គឺ index -2
            candle_5m_2nd = df_5m.iloc[-2] if len(df_5m) >= 2 else df_5m.iloc[-1]
            
            return current_price, df_5m, candle_5m_2nd
    except Exception as e:
        st.error(f"⚠️ Error fetching real-time price: {e}")
    
    # Fallback តម្លៃសាកល្បង បើសិនជាគ្មានអ៊ីនធឺណិត ឬ API មានបញ្ហា
    return st.session_state.get('simulated_market_price', 4125.00), None, None


def analyze_advanced_smc_setup():
    """
    ប្រព័ន្ធវិភាគ SMC (Hybrid Real-time Execution):
    - យកតម្លៃ Liquidity Patterns ពី OCR / Manual Input ធ្វើជាតម្លៃគោល
    - ទាញយក Live Price & 5m 2nd Candle ពី yfinance មកផ្ទៀងផ្ទាត់ Real-time ស្វ័យប្រវត្តិ
    """
    # ១. ទាញយកតម្លៃ Live Price និង 5m Candle ទី ២ ក្នុងពេលជាក់ស្តែង
    current_price, df_5m, candle_5m_2nd = fetch_realtime_gold_data()
    st.session_state['live_market_price'] = current_price

    # ២. ទាញយកទិន្នន័យ Big Pattern & Sub-Patterns ដែលបានមកពី OCR / Manual Input
    bg_max = st.session_state.get('inp_bg_range_max', 4250.00)
    bg_min = st.session_state.get('inp_bg_range_min', 4000.00)
    
    h1_min = st.session_state.get('inp_highest_rect_1_min', bg_max - 20)
    h1_max = st.session_state.get('inp_highest_rect_1_max', bg_max)
    l1_min = st.session_state.get('inp_lowest_rect_1_min', bg_min)
    l1_max = st.session_state.get('inp_lowest_rect_1_max', bg_min + 20)

    # ៣. ពិនិត្យមើលស្ថានភាព Risk Protocol (Base Building, Fakeout Trap, BO Failure)
    is_fakeout_detected = st.session_state.get('trap_detected_flag', False)
    trap_range_combined = st.session_state.get('trap_combined_range', "[4120.00 - 4165.00]")
    macro_bo_failed = st.session_state.get('macro_bo_failed_flag', False)
    is_building_base = st.session_state.get('base_building_detected', True) # 4H Base Building Status

    # ៤. លក្ខខណ្ឌ Stand Aside សរុប (បើសាង Base លើ 4H គឺលាក់ Entry រង់ចាំ Screenshot ថ្មី)
    should_stand_aside = is_fakeout_detected or macro_bo_failed or is_building_base

    # ៥. ពិនិត្យការ Swept នៃ 5m Candle ទី ២ ជាមួយ Zone ពី OCR
    is_buy_confirmed = False
    is_sell_confirmed = False

    if candle_5m_2nd is not None and not should_stand_aside:
        c_low = candle_5m_2nd['Low']
        c_high = candle_5m_2nd['High']
        c_close = candle_5m_2nd['Close']

        # Confirm Buy: ទៀន 5m ទី ២ លូន Low ចូល/Sweep Demand Zone (l1_min - l1_max) រួចបិទលើ
        if c_low <= l1_max and c_close > l1_min:
            is_buy_confirmed = True

        # Confirm Sell: ទៀន 5m ទី ២ លូន High ចូល/Sweep Supply Zone (h1_min - h1_max) រួចបិទក្រោម
        if c_high >= h1_min and c_close < h1_max:
            is_sell_confirmed = True

    # ៦. គណនា A+ Entry, SL, TP ពេលមាន 5m Confirmation
    buy_entry = round(current_price, 2)
    buy_sl = round(l1_min - 5.00, 2)
    buy_tp = round(h1_min - 10.00, 2)

    sell_entry = round(current_price, 2)
    sell_sl = round(h1_max + 5.00, 2)
    sell_tp = round(l1_max + 10.00, 2)

    # ៧. រៀបចំលទ្ធផលផ្ញើទៅ smc_execution.py
    analysis_results = {
        "current_price": current_price,
        "stand_aside": should_stand_aside,
        "fakeout_trap": is_fakeout_detected,
        "macro_bo_failed": macro_bo_failed,
        "base_building": is_building_base,
        "trap_range": trap_range_combined,
        
        # បើ Stand Aside ឬ មិនទាន់ Confirm 5m ទៀនទី 2 គឺលាក់តម្លៃ (None)
        "buy_setup": {
            "action": "BUY (LONG) - 5m 2nd Candle Confirmed",
            "entry": buy_entry,
            "sl": buy_sl,
            "tp": buy_tp,
            "risk_reward": round((buy_tp - buy_entry) / max((buy_entry - buy_sl), 0.1), 2)
        } if (not should_stand_aside and is_buy_confirmed) else None,
        
        "sell_setup": {
            "action": "SELL (SHORT) - 5m 2nd Candle Confirmed",
            "entry": sell_entry,
            "sl": sell_sl,
            "tp": sell_tp,
            "risk_reward": round((sell_entry - sell_tp) / max((sell_sl - sell_entry), 0.1), 2)
        } if (not should_stand_aside and is_sell_confirmed) else None,
        
        "proximity_alert": abs(current_price - h1_min) < 15 or abs(current_price - l1_max) < 15
    }

    st.session_state['advanced_smc_results'] = analysis_results
    return analysis_results