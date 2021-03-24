
import streamlit as st
import pandas as pd
import numpy as np



df = pd.read_csv('https://github.com/lavsz/Project-Africa_Sustainability_and_Food_Security/blob/main/Visualizations/FEWSNET_Band.csv')

st.dataframe(df.head())

