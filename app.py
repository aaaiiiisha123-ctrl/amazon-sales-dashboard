import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Amazon Sales Dashboard 📊")

df = pd.read_csv(r"C:\Users\aisha\OneDrive\Desktop\python_practice\amazon.csv\amazon.csv")
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


