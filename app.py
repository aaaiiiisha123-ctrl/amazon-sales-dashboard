import streamlit as st
import pandas as pd
import plotly.express as px 

st.title ("Amazon sales dashboard")

df = pd.read_csv(r"C:\Users\aisha\OneDrive\Desktop\python_practice\amazon.csv\amazon.csv")
st.sidebar.header("Filters")

category = st.sidebar.selectbox(
    "select category:",
    df["category"].unique()
)

filtered_df = df[df["category"] == category]
st.metric("Total Products", len(filtered_df))

st.dataframe(filtered_df)

fig = px.histogram(filtered_df, x="rating", title= "Products rating Distribution")
st.plotly_chart(fig)