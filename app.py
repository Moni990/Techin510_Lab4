import streamlit as st
import pandas as pd
import json

# Loading data from JSON
with open('books_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)
df['numeric_price'] = df['price'].str.replace('£', '').astype(float)  # Convert price to numeric for filtering

# Streamlit app interface
st.title('Book Filter App')

# Filters
name_query = st.sidebar.text_input("Search by book name")
rate_filter = st.sidebar.selectbox('Filter by rate', [0, 1, 2, 3, 4, 5], index=0)
price_filter = st.sidebar.slider('Filter by price',
                                 min_value=float(df['numeric_price'].min()),
                                 max_value=float(df['numeric_price'].max()),
                                 value=(float(df['numeric_price'].min()), float(df['numeric_price'].max())))

# Apply filters
filtered_df = df[df['name'].str.contains(name_query, case=False, na=False)] if name_query else df
filtered_df = filtered_df[filtered_df['rate'] == rate_filter] if rate_filter > 0 else filtered_df
filtered_df = filtered_df[(filtered_df['numeric_price'] >= price_filter[0]) & (filtered_df['numeric_price'] <= price_filter[1])]

# Display filtered data
st.write("Filtered Books:", filtered_df[['name', 'price', 'rate']])
