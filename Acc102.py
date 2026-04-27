import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# 1. Page Configuration & Custom CSS
# ==========================================
st.set_page_config(page_title="Pro Stock Terminal", layout="wide", page_icon="📈")

# Custom CSS for a professional "Dark Mode" financial terminal look
st.markdown("""
    <style>
    /* Global Background & Font Color */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #262b30;
        border: 1px solid #4e525a;
        padding: 5%;
        border-radius: 5px;
        overflow: hidden;
    }

    /* Hide Hamburger Menu & Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. Helper Functions
# ==========================================
@st.cache_data(ttl=600)
def load_data(ticker, start, end):
    """
    Downloads stock data from Yahoo Finance.
    """
    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        if df.empty:
            return None
        # Flatten columns if MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data(ttl=600)
def get_stock_info(ticker):
    """
    Fetches static stock info like Market Cap, P/E Ratio, etc.
    """
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except:
        return {}

def calculate_technical_indicators(df):
    """
    Calculates Moving Averages and Bollinger Bands.
    """
    # Simple Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # Bollinger Bands
    std_dev = df['Close'].rolling(window=20).std()
    df['BB_upper'] = df['SMA_20'] + (std_dev * 2)
    df['BB_lower'] = df['SMA_20'] - (std_dev * 2)
    
    return df

# ==========================================
# 3. Plotting Functions
# ==========================================
def create_chart(df, ticker):
    """
    Creates an interactive Plotly chart with Candlesticks, Volume, and Indicators.
    """
    # Calculate indicators
    df = calculate_technical_indicators(df)

    # Create Subplots: 2 rows, shared x-axis
    # Row 1: Price (Height 70%), Row 2: Volume (Height 30%)
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03, 
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{ticker} Price Action', 'Volume')
    )

    # 1. Candlestick Trace
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
            increasing_line_color='#26a69a', # Green
            decreasing_line_color='#ef5350'  # Red
        ),
        row=1, col=1
    )

    # 2. Moving Averages
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='#F6AD6F', width=1), name='SMA 20'),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='#6B86B4', width=1), name='SMA 50'),
        row=1, col=1
    )

    # 3. Bollinger Bands
    # Upper Band
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_upper'], line=dict(color='rgba(255, 165, 0, 0.3)', width=1, dash='dot'), name='BB Upper'),
        row=1, col=1
    )
    # Lower Band
    fig.add_trace(
        go.Scatter(x=df.index, y=df['BB_lower'], line=dict(color='rgba(255, 165, 0, 0.3)', width=1, dash='dot'), name='BB Lower'),
        row=1, col=1
    )

    # 4. Volume Bars
    colors = ['#26a69a' if row['Close'] >= row['Open'] else '#ef5350' for index, row in df.iterrows()]
    fig.add_trace(
        go.Bar(x=df.index, y=df['Volume'], marker_color=colors, opacity=0.5, name='Volume'),
        row=2, col=1
    )

    # Update Layout
    fig.update_layout(
        template='plotly_dark',
        xaxis_rangeslider_visible=False, # Hide default range slider to save space
        height=700,
        hovermode='x unified',
        legend=dict(orientation="h", y=1.02, x=0.01)
    )

    # Axis Labels
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig

# ==========================================
# 4. Main Application Logic
# ==========================================
st.markdown("<h1 style='text-align: center;'>📈 Pro Stock Terminal</h1>", unsafe_allow_html=True)

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("🎛️ Control Panel")
    ticker_symbol = st.text_input("Stock Ticker", value="AAPL").upper()
    
    # Date Range
    end_date = pd.Timestamp.today()
    start_date = st.date_input("Start Date", value=end_date - pd.DateOffset(years=1))
    end_date = st.date_input("End Date", value=end_date)

    st.markdown("---")
    st.markdown("### 📊 Indicators")
    show_sma = st.checkbox("Show Moving Averages", value=True)
    show_bb = st.checkbox("Show Bollinger Bands", value=True)

    st.markdown("---")
    analyze_btn = st.button("🚀 Analyze Market", use_container_width=True)

# --- Main Execution ---
if analyze_btn:
    if not ticker_symbol:
        st.warning("Please enter a ticker symbol.")
    else:
        with st.spinner(f"Fetching data for {ticker_symbol}..."):
            # 1. Load Data
            df = load_data(ticker_symbol, start_date, end_date)
            
            if df is None or df.empty:
                st.error(f"❌ Could not find data for **{ticker_symbol}**. Please check the symbol.")
            else:
                # 2. Get Info (for metrics)
                info = get_stock_info(ticker_symbol)
                
                # Extract current price safely
                current_price = df['Close'].iloc[-1]
                previous_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
                change = current_price - previous_close
                change_pct = (change / previous_close) * 100

                # --- Top Metrics ---
                m1, m2, m3, m4 = st.columns(4)
                try:
                    m1.metric("Current Price", f"${current_price:.2f}", f"{change:.2f} ({change_pct:.2f}%)")
                    m2.metric("Market Cap", f"${info.get('marketCap', 0)/1e9:.2f}B")
                    m3.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
                    m4.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 'N/A'):.2f}")
                except Exception as e:
                    st.warning("Some financial data is missing.")

                st.markdown("---")

                # --- Chart ---
                fig = create_chart(df, ticker_symbol)
                st.plotly_chart(fig, use_container_width=True)

                # ==========================================
                # 5. Qualitative Analysis Module (NEW)
                # ==========================================
                st.markdown("---")
                st.markdown("### 🧠 Qualitative Analysis")

                # Company Profile & Business
                st.markdown("#### 🏢 Company Profile & Business Model")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Basic Information**")
                    name = info.get('longName', 'N/A')
                    sector = info.get('sector', 'N/A')
                    industry = info.get('industry', 'N/A')
                    country = info.get('country', 'N/A')
                    st.write(f"- **Name:** {name}")
                    st.write(f"- **Sector:** {sector}")
                    st.write(f"- **Industry:** {industry}")
                    st.write(f"- **Country:** {country}")

                with col2:
                    st.markdown("**Management & Governance**")
                    ceo = info.get('companyOfficers', [{}])[0].get('name', 'N/A') if info.get('companyOfficers') else 'N/A'
                    employees = info.get('fullTimeEmployees', 'N/A')
                    st.write(f"- **CEO:** {ceo}")
                    st.write(f"- **Employees:** {employees:,}" if isinstance(employees, int) else f"- **Employees:** {employees}")
                
                # Business Summary
                summary = info.get('longBusinessSummary', 'Business summary not available.')
                if summary != 'N/A':
                    st.markdown(f"**Business Summary:**\n\n{summary}")
                else:
                    st.markdown("**Business Summary:** Not available.")

                # ==========================================
                # 6. Quantitative Analysis Module (FIXED)
                # ==========================================
                st.markdown("---")
                st.markdown("### 📉 Quantitative Analysis")

                # Safety check: Ensure we have enough data
                if len(df) < 2:
                    st.error("Insufficient data for quantitative analysis. Please select a longer date range.")
                else:
                    # Calculate Returns
                    df['Returns'] = df['Close'].pct_change().dropna()

                    # 1. Annualized Return
                    total_days = len(df)
                    # Handle division by zero if days is 0
                    if total_days > 0:
                        total_return = (df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1
                        # Handle cases where the period is less than a year
                        annualized_return = (1 + total_return) ** (252 / total_days) - 1 if total_days > 0 else 0
                    else:
                        annualized_return = 0

                    # 2. Annualized Volatility
                    # Check if there are enough return points
                    if len(df['Returns'].dropna()) > 1:
                        annualized_volatility = df['Returns'].std() * (252 ** 0.5)
                    else:
                        annualized_volatility = 0

                    # 3. Sharpe Ratio (Assuming Risk Free Rate = 0)
                    if annualized_volatility != 0:
                        sharpe_ratio = annualized_return / annualized_volatility
                    else:
                        sharpe_ratio = float('inf') if annualized_return > 0 else 0

                    # 4. Max Drawdown
                    try:
                        df['Cumulative_Returns'] = (1 + df['Returns']).cumprod()
                        df['Rolling_Max'] = df['Cumulative_Returns'].cummax()
                        df['Drawdown'] = (df['Cumulative_Returns'] - df['Rolling_Max']) / df['Rolling_Max']
                        max_drawdown = df['Drawdown'].min()
                    except:
                        max_drawdown = 0

                    # Display Metrics
                    qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)
                    qa_col1.metric("Annualized Return", f"{annualized_return:.1%}" if annualized_return != float('inf') else "Infinity")
                    qa_col2.metric("Annualized Volatility", f"{annualized_volatility:.1%}")
                    qa_col3.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}" if sharpe_ratio != float('inf') else "High")
                    qa_col4.metric("Max Drawdown", f"{max_drawdown:.1%}")

                    # Drawdown Chart
                    st.markdown("#### Historical Drawdown")
                    fig_dd = go.Figure()
                    # Filter out NaN values for plotting
                    valid_dd = df['Drawdown'].dropna()
                    if not valid_dd.empty:
                        fig_dd.add_trace(go.Scatter(
                            x=valid_dd.index,
                            y=valid_dd,
                            fill='tozeroy',
                            mode='lines',
                            line=dict(color='#D66FD2', width=1)
                        ))
                    else:
                        fig_dd.add_trace(go.Scatter(x=[], y=[], mode='lines'))

                    fig_dd.update_layout(
                        template='plotly_dark',
                        height=250,
                        xaxis_title="Date",
                        yaxis_title="Drawdown %",
                        showlegend=False,
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    st.plotly_chart(fig_dd, use_container_width=True)

                # ==========================================
                # 7. Raw Data Download (Original Section)
                # ==========================================
                with st.expander("View Raw Data"):
                    st.dataframe(df.sort_index(ascending=False))
                    csv = df.to_csv()
                    st.download_button("Download CSV", csv, f"{ticker_symbol}_data.csv", mime="text/csv")

else:
    st.info("👈 Enter a ticker symbol in the sidebar and click **Analyze Market** to begin.")
