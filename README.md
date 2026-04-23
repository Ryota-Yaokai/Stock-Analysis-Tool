# Stock-Analysis-Tool
This is a stock analysis tool 
# 📈 ProTrade Terminal | WRDS Financial Analytics

**ProTrade Terminal** is a professional-grade financial data analysis dashboard built with Python and Streamlit. It connects directly to the **WRDS (Wharton Research Data Services)** platform, leveraging the CRSP database to provide real-time stock price analysis, technical indicator visualization, and benchmark comparisons against the S&P 500 index.

This project is designed to offer researchers and traders a lightweight, interactive, and aesthetically pleasing tool for financial data exploration.

---

## ✨ Key Features

- **🔐 Secure Authentication**: Users can input WRDS credentials via the sidebar. The app utilizes `st.cache_resource` for efficient and secure database connection management.
- **📊 Interactive Charting**:
    - Visualizes stock closing prices alongside Moving Averages (MA).
    - Supports overlaying the **S&P 500 Index** for cumulative return benchmarking.
    - Features a volume bar chart at the bottom with color-coded price action (Green/Red).
- **📉 Deep Dive Analytics**:
    - **Return Distribution**: A histogram visualizing the distribution and mean of daily returns.
    - **Raw Data Inspection**: Displays the most recent trading data points (Price, Volume, Returns).
- **💾 Data Export**: One-click functionality to download historical data as a CSV file.
- **🎨 Dark Mode UI**: Custom CSS styling provides a professional, eye-friendly dark theme suitable for trading terminals.

---

## 🛠️ Tech Stack

- **Core Framework**: Python 3.x, Streamlit
- **Data Source**: WRDS (CRSP Databases: `dsf`, `dsi`, `msenames`)
- **Data Manipulation**: Pandas, NumPy
- **Visualization**: Matplotlib, GridSpec

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed and a valid **WRDS account** subscription.

### 2. Installation
Clone this repository and install the required Python libraries:

```bash
# Clone the repository
git clone https://github.com/your-username/ProTrade-Terminal.git

# Navigate to the directory
cd ProTrade-Terminal

# Install dependencies
pip install -r requirements.txt
