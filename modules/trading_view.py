import streamlit as st
import streamlit.components.v1 as components

def render_trading_view():
    st.subheader("📈 Live Market Chart (TradingView / MT5)")
    
    # ฝัง TradingView Widget សម្រាប់ XAUUSD (មាស)
    tradingview_widget = """
    <div class="tradingview-widget-container" style="height:550px;width:100%">
      <div id="tradingview_widget" style="height:calc(100% - 32px);width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {
        "width": "100%",
        "height": 550,
        "symbol": "OANDA:XAUUSD",
        "interval": "15",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_widget"
      }
      );
      </script>
    </div>
    """
    components.html(tradingview_widget, height=560)