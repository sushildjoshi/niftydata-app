from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st
 
# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)
# Import your data
#df = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")
df = pd.read_csv("/workspaces/niftydata-app/Walmart Data Analysis and Forcasting.csv")
dates = pd.DataFrame()
dates['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
df['Date'] = dates['Date']
pyg_app = StreamlitRenderer(df)
 
pyg_app.explorer()