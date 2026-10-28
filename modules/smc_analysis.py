import os
import json

CONFIG_FILE = "smc_manual_config.json"

def load_smc_records():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return []

def calculate_global_a_plus():
    """
    គណនារក Global A+ Pattern (Top ខ្ពស់បំផុត និង Bottom ទាបបំផុត) 
    ពីគ្រប់ Range និង Liquidity Zones ដែលបានរក្សាទុក។
    """
    records = load_smc_records()
    if not records:
        return None, None

    all_top_maxs = []
    all_bot_mins = []

    for r in records:
        for z in r.get('top', []):
            if 'max' in z:
                all_top_maxs.append(z['max'])
        for z in r.get('bottom', []):
            if 'min' in z and z['min'] > 0:
                all_bot_mins.append(z['min'])

    highest_top = max(all_top_maxs) if all_top_maxs else 0.000
    lowest_bot = min(all_bot_mins) if all_bot_mins else 0.000

    return highest_top, lowest_bot

def get_technical_signals(current_price):
    """
    ធ្វើការវិភាគបច្ចេកទេស (Technical Analysis) ដោយប្រើប្រាស់ Global A+ Zone 
    ដើម្បីផ្តល់ទិន្នន័យដល់ smc_execution យកទៅបង្ហាញ។
    """
    highest_top, lowest_bot = calculate_global_a_plus()
    
    if not highest_top or not lowest_bot:
        return {
            "status": "No Data",
            "message": "មិនទាន់มีទិន្នន័យ SMC Manual គ្រប់គ្រាន់សម្រាប់ការវិភាគ។",
            "entry": 0.0,
            "sl": 0.0,
            "tp": 0.0
        }

    # ឧទាហរណ៍នៃការគណនា Logic ផ្អែកលើ A+ Zone សម្រាប់ SL តូច (Tight SL)
    # ប្រសិនបើតម្លៃបច្ចុប្បន្នish ជិតតំបន់ Top A+ នឹងให้สัญญาณ SELL ជាមួយ SL តូច
    if current_price >= (highest_top - 5.0):
        entry = current_price
        sl = highest_top + 1.5   # Stop Loss តូចនៅเหนือ Top A+ បន្តិច
        tp = lowest_bot          # Take Profit គោលដៅនៅ Bottom A+
        signal_type = "SELL SIGNAL (PREMIUM A+ | LIQUIDITY SWEEP)"
    elif current_price <= (lowest_bot + 5.0):
        entry = current_price
        sl = lowest_bot - 1.5    # Stop Loss តូចនៅក្រោម Bottom A+ បន្តិច
        tp = highest_top         # Take Profit គោលដៅនៅ Top A+
        signal_type = "BUY SIGNAL (DISCOUNT A+ | LIQUIDITY SWEEP)"
    else:
        entry = current_price
        sl = current_price - 2.0
        tp = current_price + 4.0
        signal_type = "WAITING FOR A+ ZONE TEST"

    return {
        "status": "Active",
        "signal": signal_type,
        "entry": round(entry, 3),
        "sl": round(sl, 3),
        "tp": round(tp, 3),
        "highest_top": highest_top,
        "lowest_bot": lowest_bot
    }
