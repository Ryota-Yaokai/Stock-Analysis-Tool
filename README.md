# Pro Stock Terminal

### 1. Problem & User
Individual investors often struggle with scattered financial data and lack access to professional-grade charting tools without expensive subscriptions. This project provides a streamlined, dark-mode terminal for traders to visualize stock price action and technical indicators in one place.

### 2. Data
- **Source:** Yahoo Finance (accessed via the `yfinance` Python library).
- **Access Date:** Real-time data (fetched dynamically at runtime).
- **Key Fields:** Open, High, Low, Close (OHLC) prices, Adjusted Close, Volume, Market Cap, P/E Ratio, and 52-Week Highs.

### 3. Methods
1.  **Data Ingestion:** Used `yfinance` to download historical stock data and fundamental info based on user ticker input.
2.  **Technical Analysis:** Calculated Simple Moving Averages (SMA 20, SMA 50) and Bollinger Bands (Upper/Lower) using Pandas rolling window functions.
3.  **Visualization:** Built an interactive subplot using `Plotly.graph_objects`, combining a candlestick chart (top row) and volume bars (bottom row) with custom colors.
4.  **UI Implementation:** Developed the frontend using `Streamlit`, including custom CSS for a dark theme and sidebar controls for date ranges and indicators.

### 4. Key Findings
-   **Visual Clarity:** Overlaying SMA lines on candlestick charts allows users to instantly identify trend directions (uptrend vs. downtrend).
-   **Volatility Indicators:** Bollinger Bands effectively highlight periods of high volatility (bands widening) vs. low volatility (bands squeezing).
-   **Performance:** Using `@st.cache_data` significantly reduces API load times and prevents redundant data fetching during user interaction.
-   **User Experience:** A "Dark Mode" interface reduces eye strain, which is preferred by traders who spend long hours analyzing charts.

### 5. How to run
To run this project locally, you need Python installed.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install dependencies:**
    ```bash
    pip install streamlit yfinance pandas plotly
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

### 6. Product link / Demo
-   Here is the link of app:https://stock-analysis-tool-bkpgfdbnpd4uwyojsfg9mm.streamlit.app/

### 7. Limitations & next steps
-   **Limitations:** The current version relies solely on `yfinance`, which may have occasional rate limits or data delays. The technical analysis is limited to basic indicators (SMA, Bollinger Bands).
-   **Next Steps:**
    -   Add more complex indicators like RSI (Relative Strength Index) and MACD.
    -   Implement a sentiment analysis feature using news headlines.
    -   Add a "Compare" feature to overlay multiple tickers on the same chart.
