
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Amazon Sales Dashboard 📊")

df = pd.read_csv("amazon.csv/amazon.csv")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"].str.replace("%", ""), errors="coerce"
)

st.sidebar.header("Filters")

category = st.sidebar.selectbox("Select Category:", df["category"].unique())
min_rating = st.sidebar.slider("Minimum Rating:", 0.0, 5.0, 3.0)
min_discount = st.sidebar.slider("Minimum Discount %:", 0, 100, 0)

filtered_df = df[df["category"] == category]
filtered_df = filtered_df[filtered_df["rating"] >= min_rating]
filtered_df = filtered_df[filtered_df["discount_percentage"] >= min_discount]

st.metric("Total Products", len(filtered_df))
st.dataframe(filtered_df)

fig = px.histogram(filtered_df, x="rating", title="Products Rating Distribution")
st.plotly_chart(fig)

st.subheader("Top Products by Rating")
top_products = filtered_df.nlargest(10, "rating")
fig2 = px.bar(top_products, x="product_name", y="rating", title="Top 10 Products")
st.plotly_chart(fig2)

#create a profit analysis feature in this 
st.subheader("Profit Analysis")
df["actual_price"] = pd.to_numeric(
    df["actual_price"].str.replace("₹","").str.replace(",",""),
    errors="coerce"
)
df["discounted_price"] = pd.to_numeric(
    df["discounted_price"].str.replace("₹","").str.replace(",",""),
    errors="coerce"
)

df["profit"] = df["actual_price"]-df["discounted_price"]
category_profit = df.groupby("category")["profit"].mean()

#create bar chart for profit analysis
fig3  = px.bar(
    category_profit.reset_index(),
    x="category",
    y="profit",
    title="category wise profit analysis"
)
st.plotly_chart(fig3)

import numpy as np
from sklearn.ensemble import RandomForestRegressor


# Fresh data load karo sirf ML ke liye
df_ml = pd.read_csv("amazon.csv/amazon.csv")

df_ml["actual_price"] = pd.to_numeric(
    df_ml["actual_price"].str.replace("₹","").str.replace(",",""),
    errors="coerce"
)
df_ml["discount_percentage"] = pd.to_numeric(
    df_ml["discount_percentage"].str.replace("%",""),
    errors="coerce"
)
df_ml["rating"] = pd.to_numeric(df_ml["rating"], errors="coerce")
df_ml["rating_count"] = pd.to_numeric(
    df_ml["rating_count"].str.replace(",",""),
    errors="coerce"
)

df_ml = df_ml.dropna(subset=["actual_price","discount_percentage","rating","rating_count"])

X = df_ml[["discount_percentage","rating","rating_count"]]
y = df_ml["actual_price"]


model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

user_discount = st.slider("Discount %:", 0, 90, 10)
user_rating = st.slider("Rating:", 1.0, 5.0, 3.0)
user_rating_count = st.number_input("Rating Count:", value=100)

predicted_price = model.predict([[user_discount, user_rating, user_rating_count]])
st.metric("Predicted Price", f"₹{predicted_price[0]:.2f}")