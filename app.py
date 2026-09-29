import pandas as pd
import streamlit as st

# 1. Page Configuration (Wide Layout)
st.set_page_config(
    page_title="Bank Marketing Campaign Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling for a cleaner look
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        .metric-card { background-color: #262730; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 Bank Marketing Campaign Analytics Dashboard")
st.markdown("Interactive analytics interface evaluating customer demographics, account balances, and campaign performance across multiple dimensions.")

# 2. Load Dataset
@st.cache_data
def load_banking_data():
    df = pd.read_csv("train.csv", sep=";")
    
    # Preprocess Age into Age Groups to satisfy age filtering requirements
    if "age" in df.columns:
        bins = [0, 25, 35, 50, 65, 120]
        labels = ["<25", "25-35", "36-50", "51-65", "65+"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
        
    return df

try:
    df = load_banking_data()

    # 3. Sidebar Filters (Expanding to 5 Distinct Characteristics per Project Requirements)
    st.sidebar.header("🔍 Multi-Characteristic Filters")
    st.sidebar.markdown("Filter campaign data across 5 key dimensions:")

    # Characteristic 1: Job / Occupation
    job_options = ["All"] + list(df["job"].unique()) if "job" in df.columns else ["All"]
    selected_job = st.sidebar.selectbox("1. Occupation / Job", options=job_options)

    # Characteristic 2: Age Group
    age_options = ["All"] + list(df["age_group"].dropna().unique()) if "age_group" in df.columns else ["All"]
    selected_age = st.sidebar.selectbox("2. Age Group", options=age_options)

    # Characteristic 3: Education Level
    edu_options = ["All"] + list(df["education"].unique()) if "education" in df.columns else ["All"]
    selected_edu = st.sidebar.selectbox("3. Education Level", options=edu_options)

    # Characteristic 4: Contact Method
    contact_options = ["All"] + list(df["contact"].unique()) if "contact" in df.columns else ["All"]
    selected_contact = st.sidebar.selectbox("4. Contact Method", options=contact_options)

    # Characteristic 5: Previous Outcome
    poutcome_options = ["All"] + list(df["poutcome"].unique()) if "poutcome" in df.columns else ["All"]
    selected_poutcome = st.sidebar.selectbox("5. Previous Outcome", options=poutcome_options)

    # Apply all filters sequentially
    filtered_df = df.copy()
    if selected_job != "All":
        filtered_df = filtered_df[filtered_df["job"] == selected_job]
    if selected_age != "All":
        filtered_df = filtered_df[filtered_df["age_group"] == selected_age]
    if selected_edu != "All":
        filtered_df = filtered_df[filtered_df["education"] == selected_edu]
    if selected_contact != "All":
        filtered_df = filtered_df[filtered_df["contact"] == selected_contact]
    if selected_poutcome != "All":
        filtered_df = filtered_df[filtered_df["poutcome"] == selected_poutcome]

    # 4. Top KPI Summary Cards
    st.markdown("### 📊 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)

    total_customers = len(filtered_df)
    avg_balance = filtered_df["balance"].mean() if "balance" in filtered_df.columns else 0
    
    # Checking subscription outcome column ('y')
    success_col = "y" if "y" in filtered_df.columns else ("response" if "response" in filtered_df.columns else None)
    
    if success_col and total_customers > 0:
        success_count = filtered_df[filtered_df[success_col].astype(str).str.lower().isin(["yes", "1", "true"])].shape[0]
        success_rate = (success_count / total_customers) * 100
    else:
        success_rate = 0.0

    col1.metric("Filtered Customer Count", f"{total_customers:,}")
    col2.metric("Average Account Balance", f"${avg_balance:,.2f}")
    col3.metric("Campaign Success / Conversion Rate", f"{success_rate:.2f}%")

    st.divider()

    # 5. Advanced Visualizations Layout
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("💰 Average Account Balance by Job")
        if "job" in filtered_df.columns and "balance" in filtered_df.columns:
            chart_data_balance = filtered_df.groupby("job")["balance"].mean().sort_values(ascending=False)
            st.bar_chart(chart_data_balance)
        else:
            st.info("Required data columns for balance breakdown unavailable.")

    with col_right:
        st.subheader("🎯 Campaign Outcomes Distribution")
        if success_col and "job" in filtered_df.columns:
            outcome_data = pd.crosstab(filtered_df["job"], filtered_df[success_col])
            st.bar_chart(outcome_data)
        else:
            st.info("Outcome column breakdown unavailable.")

    # 6. Data Preview Section
    with st.expander("📂 View Raw Filtered Data Table"):
        st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading or processing dataset: {e}. Please ensure 'train.csv' is in your root directory.")