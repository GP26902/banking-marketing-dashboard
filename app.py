import streamlit as st
import pandas as pd

st.title("Banking Marketing Campaign Analytics Dashboard")
st.write("Welcome to the analytics dashboard. Below is a preview of the training dataset:")

# Load the training data 
@st.cache_data
def load_data():
    return pd.read_csv("train.csv", sep=";")

df = load_data()

# Show dataset metrics
st.metric(label="Total Rows", value=df.shape[0])
st.metric(label="Total Columns", value=df.shape[1])

# Display the data frame
st.dataframe(df.head(10))