import os
import json
import pandas as pd
import MetaTrader5 as MT5

# ទីតាំងឯកសារ Config និង History State
CONFIG_FILE_ROOT = os.path.join(os.path.dirname(__file__), "..", "smc_manual_config.json")
HISTORY_STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "configs", "macro_history_state.json")

def load_json_file(filepath):
    """អនុគមន៍ទូទៅសម្រាប់អានឯកសារ JSON"""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def get_system_trading_status():
    """ពិនិត្យមើលតម្លៃ trading_enabled ពីไฟล์ Config"""
    data = load_json_file(CONFIG_FILE_ROOT)
    if isinstance(data, dict):
        return data.get("system_status", {}).get("trading_enabled", True)
    return True

def load_manual_config():
    """ទាញយកការកំណត់ Range ពី Manual Config"""
    data = load_json_file(CONFIG_FILE_ROOT)
    if isinstance(data, dict):
        records = data.get("records", [])
        if records:
            return records
    if isinstance(data, list):
        return data
    return []

def load_macro_history():
    """ទាញយកប្រវត្តិសាស្ត្រ Macro History State (Top/Bottom Liquidity Sweeps)"""
    return load_json_file(HISTORY_STATE_FILE)

def fetch_mt5_data(symbol="XAUUSD"):
    """ទាញយកទិន្នន័យតម្លៃពី MetaTrader 5 (M15 និង M5)"""
    if not MT5.initialize():
        return None, None, 0.000

    tick = MT5.symbol_info_tick(symbol)
    current_price = tick.bid if tick is not None else 0.000

    m15_rates = MT5.copy_rates_from_pos(symbol, MT5.TIMEFRAME_M15, 0, 20)
    m5_rates = MT5.copy_rates_from_pos(symbol, MT5.TIMEFRAME_M5, 0, 30)
    MT5.shutdown()

    df_m15 = pd.DataFrame(m15_rates) if m15_rates is not None else pd.DataFrame()
    df_m5 = pd.DataFrame(m5_rates) if m5_rates is not None else pd.DataFrame()

    return df_m15, df_m5, float(current_price)

def get_active_range_limits():
    """ទាញយកតម្លៃ Range Min និង Range Max ពី Manual Config"""
    records = load_manual_config()
    for rec in records:
        if rec.get("pattern") in ["A", "A2"] and rec.get("range_min", 0) > 4100:
            return rec.get("range_min"), rec.get("range_max")
    if records:
        first = records[0]
        return first.get("range_min", 4104.405), first.get("range_max", 4144.015)
    return 4104.405, 4144.015

def format_precision(value):
    """จัดតម្រៀបទម្រង់លេខឱ្យបាន 3 ខ្ទង់ច្បាស់លាស់"""
    return round(float(value), 3)

def get_technical_signals(symbol="XAUUSD"):
    """មុខងារស្នូលវិភាគសញ្ញា Hybrid SMC ជាមួយ System Toggle Check"""
    
    # 0. ពិនិត្យមើល System Toggle (បើបិទ គឺបង្ខំឱ្យ WAIT ភ្លាមៗ)
    if not get_system_trading_status():
        return {
            "current_price": 0.000,
            "macro_pattern": "NONE",
            "macro_top": 0.000,
            "macro_bottom": 0.000,
            "signal": "WAIT",
            "entry": 0.000,
            "sl": 0.000,
            "sl_color": "#FF0000",
            "tp1": 0.000,
            "tp2": 0.000,
            "tp3": 0.000,
            "active_chain_count": 0
        }

    df_m15, df_m5, current_price = fetch_mt5_data(symbol)
    range_min, range_max = get_active_range_limits()
    
    # អានប្រវត្តិសាស្ត្រលូកយក Liquidity ពី macro_history_state.json
    history_state = load_macro_history()
    pattern_history = history_state.get("A", {})
    top_swept = pattern_history.get("swept_top", False)
    bottom_swept = pattern_history.get("swept_bottom",-False) if isinstance(pattern_history.get("swept_bottom"), bool) else False
    
    signal = "WAIT"
    entry = 0.000
    calculated_sl = 0.000

    if df_m15 is not None and len(df_m15) > 0:
        m15_latest = df_m15.iloc[-1]
        
        if current_price < range_min:
            signal = "WAIT"
        elif current_price >= range_min or m15_latest['close'] >= range_min:
            if not (top_swept and bottom_swept):
                signal = "BUY"
                entry = format_precision(range_min)
                calculated_sl = format_precision(range_min - 5.0)
            else:
                signal = "WAIT"

    return {
        "current_price": format_precision(current_price),
        "macro_pattern": "A2",
        "macro_top": format_precision(range_max),
        "macro_bottom": format_precision(range_min),
        "signal": signal,
        "entry": entry,
        "sl": calculated_sl,
        "sl_color": "#FF0000",
        "tp1": format_precision(range_max),
        "tp2": format_precision(range_max + 10.0),
        "tp3": format_precision(range_max + 20.0),
        "active_chain_count": 1 if signal != "WAIT" else 0
    }