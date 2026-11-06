import time
from broker_config import BROKER_SETTINGS
from modules.smc_analysis import get_technical_signals

def run_headless_bot():
    print("==================================================")
    print("⚡ IRONCLAD CAPITAL - HEADLESS BOT ENGINE RUNNING")
    print(f"🔗 Connected Broker: {BROKER_SETTINGS['broker_name']}")
    print(f"🎯 Target Symbol: {BROKER_SETTINGS['symbol']}")
    print("==================================================")
    
    while True:
        try:
            symbol = BROKER_SETTINGS['symbol']
            data = get_technical_signals(symbol)
            
            print(f"\n[⏱️ Live Update] {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   🔹 Price: {data['current_price']:.3f}")
            print(f"   🔸 Signal: {data['signal']}")
            print(f"   📊 Entry: {data['entry']:.3f} | SL: {data['sl']:.3f} | TP1: {data['tp1']:.3f} | TP2: {data['tp2']:.3f}")

        except Exception as e:
            print(f"⚠️ Bot Loop Error: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    run_headless_bot()