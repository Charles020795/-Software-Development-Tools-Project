
import streamlit as st
import pandas as pd
import plotly.express as px

#Page configuration
st.set_page_config(page_title="Vehicle Market Analysis Dashboard", page_icon="🚗", layout="wide")
st.title("Vehicle Market Analysis Dashboard 🚗")
st.header("Analyzing Vehicle Listings")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('vehicles_us.csv')
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    df['year_posted'] = df['date_posted'].dt.year
    df['month_posted'] = df['date_posted'].dt.month
    return df

df = load_data()

#sidebar filters
st.sidebar.header("Filters and Options")    

vehicle_types = ['All'] + list(df['type'].dropna().unique())
selected_type = st.sidebar.selectbox("Select Vehicle Type:", vehicle_types)
if selected_type != 'All':
    filtered_df = df[df['type'] == selected_type]
else:
    filtered_df = df


min_price = int(df['price'].min())
max_price = int(df['price'].max())
price_range = st.sidebar.slider(
    "Price Range:",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)
filtered_df = filtered_df[
    (filtered_df['price'] >= price_range[0]) & 
    (filtered_df['price'] <= price_range[1])
]



#basic stats
st.header("📊 Market Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Listings", len(filtered_df))

with col2:
    avg_price = filtered_df['price'].mean()
    st.metric("Average Price", f"${avg_price:,.0f}")

with col3:
    avg_odometer = filtered_df['odometer'].mean()
    st.metric("Avg Odometer", f"{avg_odometer:,.0f} miles")

with col4:
    avg_days_listed = filtered_df['days_listed'].mean()
    st.metric("Avg Days Listed", f"{avg_days_listed:.0f} days")


#visualizations
st.header("💰 Price Distribution")
price_hist = px.histogram(
    filtered_df,
    x='price',
    nbins=50,
    color='model',
    title=f"Distribution of Vehicle Prices ({selected_type})",
    labels={'price': 'Price ($)'},
)
price_hist.update_layout(
    xaxis_title="Price ($)",
    yaxis_title="Number of Vehicles"
)
st.plotly_chart(price_hist, use_container_width=True)

st.header("📈 Price vs Odometer Relationship")
scatter_fig = px.scatter(
    filtered_df,
    x='odometer',
    y='price',
    color='type',
    title="Vehicle Price vs Odometer Reading",
    labels={
        'odometer': 'Odometer (miles)',
        'price': 'Price ($)',
        'type': 'Vehicle Type'
    },
    hover_data=['model_year', 'model']
)
scatter_fig.update_layout(
    xaxis_title="Odometer (miles)",
    yaxis_title="Price ($)"
)
st.plotly_chart(scatter_fig, use_container_width=True)


show_advanced_analysis = st.checkbox("Show Advanced Analysis")

if show_advanced_analysis:
    st.header("🔍 Advanced Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year_price_fig = px.box(
            filtered_df,
            x='model_year',
            y='price',
            title="Price Distribution by Model Year"
        )
        st.plotly_chart(year_price_fig, use_container_width=True)
    
    with col2:
    
        condition_price_fig = px.box(
            filtered_df,
            x='condition',
            y='price',
            title="Price Distribution by Vehicle Condition"
        )
        st.plotly_chart(condition_price_fig, use_container_width=True)


show_raw_data = st.sidebar.checkbox("Show Raw Data")
if show_raw_data:
    st.header("📋 Raw Data")
    st.dataframe(filtered_df)

st.sidebar.header("About")
st.sidebar.info(
    "This dashboard analyzes vehicle listings data to provide insights "
    "into market trends, pricing, and vehicle characteristics."
)