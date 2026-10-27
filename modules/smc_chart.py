import streamlit as st
import plotly.graph_objects as go
import yfinance as yf

def render_analytical_chart():
    st.subheader("📊 SMC Analytical Chart (Interactive Layer Controls)")

    # 1. ប៊ូតុង Toggle Control បើក/បិទ Layers លើ Chart
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)
    with ctrl_col1:
        show_big_range = st.toggle(" Big Range", value=True)
    with ctrl_col2:
        show_big_rects = st.toggle(" Big Liquidity Zones", value=True)
    with ctrl_col3:
        show_sub_zones = st.toggle(" Sub-Patterns (1-6)", value=True)

    # 2. ទាញយកទិន្នន័យ Candle 4H ជាមួយ Spinner ពេល Internet យឺត
    @st.cache_data(ttl=60)
    def get_chart_data():
        try:
            ticker = yf.Ticker("GC=F")
            df = ticker.history(period="60d", interval="4h")
            return df if not df.empty else None
        except Exception:
            return None

    with st.spinner("⏳ កំពុងទាញយកទិន្នន័យ Candle 4H និងគណនា SMC Zones..."):
        df = get_chart_data()

    if df is None or df.empty:
        st.error("⚠️ មិនអាចទាញយកទិន្នន័យក្រាហ្វបានទេ! សូមពិនិត្យមើលការភ្ជាប់ Internet របស់បង។")
        return

    # 3. Adjust Ratio Scale ឱ្យត្រូវគ្នានឹងកម្រិតតម្លៃ 4,000+
    bg_range_max = st.session_state.get('inp_bg_range_max', 4250.00)
    bg_min = st.session_state.get('inp_bg_range_min', 4000.00)
    latest_close = df['Close'].iloc[-1]
    
    if latest_close < 3500 and bg_range_max > 3500:
        ratio = bg_range_max / latest_close
        df['Open'] = df['Open'] * ratio
        df['High'] = df['High'] * ratio
        df['Low'] = df['Low'] * ratio
        df['Close'] = df['Close'] * ratio

    # 4. បង្កើត Candlestick Chart (Dark Theme)
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        increasing_line_color='#26a69a',
        decreasing_line_color='#ef5350',
        name="XAUUSD 4H"
    )])

    shapes = []

    # ==========================================
    # 📌 A. BIG PATTERN LIQUIDITY ZONES
    # ==========================================
    if show_big_range:
        # Big Pattern Range Background
        shapes.append(dict(
            type="rect", xref="paper", yref="y", x0=0, x1=1,
            y0=min(bg_min, bg_range_max), y1=max(bg_min, bg_range_max),
            fillcolor="rgba(255, 255, 255, 0.02)",
            line=dict(color="rgba(255, 255, 255, 0.2)", width=1, dash="dot"),
        ))

    if show_big_rects:
        # Highest Rectangles 1, 2, 3 (Supply / ពណ៌ក្រហម)
        colors_highest = ["rgba(231, 76, 60, 0.20)", "rgba(231, 76, 60, 0.35)", "rgba(231, 76, 60, 0.50)"]
        for i in range(1, 4):
            h_min = st.session_state.get(f'inp_highest_rect_{i}_min', 0)
            h_max = st.session_state.get(f'inp_highest_rect_{i}_max', 0)
            if h_min > 0 and h_max > 0:
                shapes.append(dict(
                    type="rect", xref="paper", yref="y", x0=0, x1=1,
                    y0=min(h_min, h_max), y1=max(h_min, h_max),
                    fillcolor=colors_highest[i-1],
                    line=dict(color="#e74c3c", width=1.5),
                ))

        # Lowest Rectangles 1, 2, 3 (Demand / ពណ៌បៃតង)
        colors_lowest = ["rgba(46, 204, 113, 0.20)", "rgba(46, 204, 113, 0.35)", "rgba(46, 204, 113, 0.50)"]
        for i in range(1, 4):
            l_min = st.session_state.get(f'inp_lowest_rect_{i}_min', 0)
            l_max = st.session_state.get(f'inp_lowest_rect_{i}_max', 0)
            if l_min > 0 and l_max > 0:
                shapes.append(dict(
                    type="rect", xref="paper", yref="y", x0=0, x1=1,
                    y0=min(l_min, l_max), y1=max(l_min, l_max),
                    fillcolor=colors_lowest[i-1],
                    line=dict(color="#2ecc71", width=1.5),
                ))

    # ==========================================
    # 📌 B. 6 SUB-PATTERNS LIQUIDITY ZONES
    # ==========================================
    if show_sub_zones:
        for sub_idx in range(1, 7):
            # Sub-Pattern Range Background
            sub_r_min = st.session_state.get(f'inp_sub_{sub_idx}_range_min', 0)
            sub_r_max = st.session_state.get(f'inp_sub_{sub_idx}_range_max', 0)
            if sub_r_min > 0 and sub_r_max > 0:
                shapes.append(dict(
                    type="rect", xref="paper", yref="y", x0=0, x1=1,
                    y0=min(sub_r_min, sub_r_max), y1=max(sub_r_min, sub_r_max),
                    fillcolor="rgba(155, 89, 182, 0.05)",
                    line=dict(color="rgba(155, 89, 182, 0.3)", width=1, dash="dashdot"),
                ))

            # Top Rectangles (ពណ៌លឿង)
            for i in range(1, 4):
                t_min = st.session_state.get(f'inp_sub_{sub_idx}_top_rect_{i}_min', 0)
                t_max = st.session_state.get(f'inp_sub_{sub_idx}_top_rect_{i}_max', 0)
                if t_min > 0 and t_max > 0:
                    shapes.append(dict(
                        type="rect", xref="paper", yref="y", x0=0, x1=1,
                        y0=min(t_min, t_max), y1=max(t_min, t_max),
                        fillcolor="rgba(241, 196, 15, 0.25)",
                        line=dict(color="#f1c40f", width=1, dash="dash"),
                    ))

            # Bottom Rectangles (ពណ៌ខៀវ)
            for i in range(1, 4):
                b_min = st.session_state.get(f'inp_sub_{sub_idx}_bottom_rect_{i}_min', 0)
                b_max = st.session_state.get(f'inp_sub_{sub_idx}_bottom_rect_{i}_max', 0)
                if b_min > 0 and b_max > 0:
                    shapes.append(dict(
                        type="rect", xref="paper", yref="y", x0=0, x1=1,
                        y0=min(b_min, b_max), y1=max(b_min, b_max),
                        fillcolor="rgba(52, 152, 219, 0.25)",
                        line=dict(color="#3498db", width=1, dash="dash"),
                    ))

    # 5. Layout Settings
    min_y = min(df['Low'].min(), bg_min) - 20
    max_y = max(df['High'].max(), bg_range_max) + 20

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#131722",
        plot_bgcolor="#131722",
        height=560,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_rangeslider_visible=False,
        yaxis=dict(range=[min_y, max_y]),
        shapes=shapes
    )

    st.plotly_chart(fig, use_container_width=True)