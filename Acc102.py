
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(page_title="🇺🇸 US Stock Analyzer", layout="wide")

# Custom CSS to hide the Streamlit menu and footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Sidebar - Control Panel
# ==========================================
st.sidebar.header("⚙️ Control Panel")

ticker_symbol = st.sidebar.text_input("Stock Ticker (US Market)", value="AAPL")

# Date Range Logic
today = pd.Timestamp.today().normalize()
one_year_ago = today - pd.DateOffset(years=1)

start_date = st.sidebar.date_input("Start Date", value=one_year_ago, min_value=pd.to_datetime("2010-01-01"))
end_date = st.sidebar.date_input("End Date", value=today, min_value=start_date)

# Options
show_candlestick = st.sidebar.checkbox("Show Candlestick Chart", value=True)
show_benchmark = st.sidebar.checkbox("Compare with S&P 500 (^GSPC)", value=True)
show_raw_data = st.sidebar.checkbox("Show Raw Data", value=True)
enable_download = st.sidebar.checkbox("Enable Download", value=True)

# ==========================================
# 3. Data Loading Function
# ==========================================
@st.cache_data(ttl=600)
def load_data(ticker, start, end):
    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty:
            return None
        df.columns = df.columns.get_level_values(0) # Flatten columns
        return df
    except Exception:
        return None

# ==========================================
# 4. Plotting Functions
# ==========================================
def plot_candlestick(df, ticker):
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['red' if row['Close'] >= row['Open'] else 'green' for index, row in df.iterrows()]
    
    # Draw candles
    for i in range(len(df)):
        ax.vlines(df.index[i], df['Low'][i], df['High'][i], color=colors[i], alpha=0.5)
        body_height = abs(df['Close'][i] - df['Open'][i])
        if body_height == 0: body_height = 0.001
        ax.bar(df.index[i], body_height, bottom=min(df['Open'][i], df['Close'][i]), 
               color=colors[i], width=0.6, alpha=0.8)

    ax.set_title(f"{ticker} Price Action (Red=Up, Green=Down)", fontsize=16)
    ax.set_ylabel("Price (USD)")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- 修改后的对比绘图函数 ---
def plot_comparison(series_stock, series_bench, name_stock, name_bench="S&P 500"):
    # 1. 合并数据并处理缺失值 (Inner Join 确保日期对齐)
    df_plot = pd.concat([series_stock, series_bench], axis=1, join='inner').dropna()
    df_plot.columns = ['Stock', 'Benchmark']
    
    if df_plot.empty:
        st.warning("No overlapping data dates found for comparison.")
        return

    # 2. 归一化 (Normalize to 100)
    df_plot['Stock_Norm'] = (df_plot['Stock'] / df_plot['Stock'].iloc[0]) * 100
    df_plot['Bench_Norm'] = (df_plot['Benchmark'] / df_plot['Benchmark'].iloc[0]) * 100

    # 3. 绘图
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_plot.index, df_plot['Stock_Norm'], label=f"{name_stock}", color='#1f77b4', linewidth=2)
    ax.plot(df_plot.index, df_plot['Bench_Norm'], label=f"{name_bench}", color='gray', linestyle='--', alpha=0.7)
    
    ax.set_title(f"Performance Comparison (Base 100)", fontsize=16)
    ax.set_ylabel("Indexed Return (%)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    
    st.pyplot(fig)

# ==========================================
# 5. Main Application Logic
# ==========================================
st.title(f"📈 US Stock Analyzer: {ticker_symbol.upper()}")

if st.button("🔍 Analyze Stock"):
    with st.spinner(f"Fetching data for {ticker_symbol}..."):
        # 1. 获取主股票数据
        stock_df = load_data(ticker_symbol, start_date, end_date)
        
        if stock_df is None or stock_df.empty:
            st.error(f"❌ Failed to load data for **{ticker_symbol}**. Please check the ticker symbol or date range.")
            st.info("💡 Tip: Ensure the End Date is not in the future (try yesterday) and the Ticker is valid (e.g., AAPL, TSLA).")
        else:
            st.success(f"Data loaded successfully for **{ticker_symbol}**")
            
            # 2. 显示指标
            latest_price = stock_df['Close'].iloc[-1]
            start_price = stock_df['Close'].iloc[0]
            price_change = latest_price - start_price
            pct_change = (price_change / start_price) * 100
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Latest Price", f"${latest_price:.2f}")
            col2.metric("Period Change", f"{price_change:.2f}", f"{pct_change:.2f}%")
            col3.metric("Total Volume", f"{int(stock_df['Volume'].sum()):,}")
            
            # 3. K线图
            if show_candlestick:
                st.subheader("Price Chart")
                plot_candlestick(stock_df, ticker_symbol)
            
            # 4. 标普500对比 (修复后的逻辑)
            if show_benchmark:
                st.subheader("Benchmark Analysis")
                # 获取标普数据
                sp500_df = load_data("^GSPC", start_date, end_date)
                
                if sp500_df is not None and not sp500_df.empty:
                    # 只传递 'Close' 列给绘图函数，避免列名冲突
                    plot_comparison(
                        stock_df['Close'], 
                        sp500_df['Close'], 
                        ticker_symbol, 
                        "S&P 500 (^GSPC)"
                    )
                else:
                    st.warning("Could not load S&P 500 data, skipping comparison.")
            
            # 5. 原始数据
            if show_raw_data:
                st.subheader("Raw Historical Data")
                st.dataframe(stock_df.sort_index(ascending=False), use_container_width=True)
                
                if enable_download:
                    csv = stock_df.to_csv()
                    st.download_button(
                        label="💾 Download Data as CSV",
                        data=csv,
                        file_name=f'{ticker_symbol}_history.csv',
                        mime='text/csv',
                    )

else:
    st.info("👈 Please adjust settings in the sidebar and click **Analyze Stock** to begin.")
    
