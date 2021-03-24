
import streamlit as st
import pandas as pd
import numpy as np



df = pd.read_csv('https://github.com/lavsz/Project-Africa_Sustainability_and_Food_Security/blob/main/Visualizations/social_conlict_hfic_raw.csv')

st.dataframe(df.head())

