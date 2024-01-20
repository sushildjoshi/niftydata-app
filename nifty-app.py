import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('Nifty 500 App')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("""
This app retrieves the list of the **nifty 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
- On the left hand side, by default all the sectors will be selected when you launch this app first time.
- Second input feature is to show stock closing price.For this you can use slider to select number of companies & then click on **Show Plots** button.
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/NIFTY_500).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
#
@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/NIFTY_500'
    html = pd.read_html(url, header = 0)
    df = html[2]
    return df

df = load_data()
sector = df.groupby('Industry')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['Industry'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['Industry'].isin(selected_sector)) ]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download nifty500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="nifty.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

# Append ".NS" to each symbol
symbols_with_suffix = [symbol + ".NS" for symbol in list(df_selected_sector[:10].Symbol)]


data = yf.download(
        tickers = symbols_with_suffix,
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol


def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot()

num_company = st.sidebar.slider('Number of Companies', 1, 10)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for symbol in symbols_with_suffix[:num_company]:
        price_plot(symbol)  # Pass 'data' argument to price_plot function
