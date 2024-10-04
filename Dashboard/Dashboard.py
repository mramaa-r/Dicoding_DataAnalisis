import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import path

# Set seaborn style for better visualization
sns.set(style="whitegrid")

# Load the merged dataset
@st.cache_data
def load_data():
    return pd.read_csv('main_data.csv')

# Load dataset
data = load_data()

# Display the title of the Streamlit app
st.title("Brazilian E-Commerce Data Analysis")

# Display the raw merged data
st.header("Merged Dataset")
st.write(data.head())  # Show top rows of the merged dataset

# Question 1: Visualisasi produk yang sering di komplain
st.header("Produk yang Sering Dikeluhkan")

# Filter data komplain (review score <= 2)
komplain = data[data['review_score'] <= 2]

# Group by product_id to get the number of complaints per product
komplain_produk = komplain.groupby('product_id').size().reset_index(name='complaints_count')

# Merge with product category
komplain_produk = pd.merge(komplain_produk, data[['product_id', 'product_category_name']].drop_duplicates(), on='product_id', how='inner')

# Sort products by complaints
komplain_produk_sorted = komplain_produk.sort_values(by='complaints_count', ascending=False)

# Display top 10 most complained products
st.subheader("Top 10 Produk yang Sering Di Komplain")
st.write(komplain_produk_sorted.head(10))

# Visualisasi komplain menggunakan bar plot
plt.figure(figsize=(10, 6))
sns.barplot(data=komplain_produk_sorted.head(10), x='complaints_count', y='product_category_name', palette='Reds_r')
plt.title('Top 10 Produk yang Sering Di Komplain')
plt.xlabel('Jumlah Komplain')
plt.ylabel('Kategori Produk')

# Show the plot in Streamlit
st.pyplot(plt)

# Question 2: Prediksi Penjualan (melihat tren penjualan bulanan)
st.header("Analisis Penjualan Bulanan")

# Convert order_purchase_timestamp to datetime if not already
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])

# Create a new column for the month of each order
data['order_purchase_month'] = data['order_purchase_timestamp'].dt.to_period('M')

# Group data by month to calculate the number of sales per month
monthly_sales = data.groupby('order_purchase_month').size()

# Visualisasi penjualan bulanan menggunakan line plot
plt.figure(figsize=(12, 6))
monthly_sales.plot()
plt.title('Penjualan Bulanan')
plt.ylabel('Jumlah Pesanan')
plt.xlabel('Bulan')
plt.grid(True)

# Show the plot in Streamlit
st.pyplot(plt)

# Footer
st.write("Dicoding Course Data Analisis")
