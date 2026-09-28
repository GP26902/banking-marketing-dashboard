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
st.markdown("Interactive analytics interface evaluating customer demographics, account balances, and campaign performance.")


# 2. Load Dataset
@st.cache_data
def load_banking_data():
  # Adjust file name/path if your CSV has a specific name in your repository
  return pd.read_csv("train.csv", sep=";")  # UCI dataset often uses semicolons


try:
    df = load_banking_data()

    # 3. Sidebar Filters
    st.sidebar.header("🔍 Filter Controls")
    
    # Multi-select or Selectbox for Job Categories
    job_options = ["All"] + list(df["job"].unique())
    selected_job = st.sidebar.selectbox("Filter by Job Category", options=job_options)

    if selected_job != "All":
        filtered_df = df[df["job"] == selected_job]
    else:
        filtered_df = df

    # 4. Top KPI Summary Cards
    st.markdown("### 📊 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)

    total_customers = len(filtered_df)
    avg_balance = filtered_df["balance"].mean()
    # Assuming 'y' column tracks subscription outcome ('yes'/'no')
    success_rate = (
        (filtered_df["y"] == "yes").sum() / total_customers * 100
    ) if total_customers > 0 else 0

    col1.metric("Total Customers in View", f"{total_customers:,}")
    col2.metric("Average Account Balance", f"${avg_balance:,.2f}")
    col3.metric("Campaign Success Rate", f"{success_rate:.2f}%")

    st.divider()

    # 5. Advanced Visualizations Layout
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("💰 Average Account Balance by Job")
        chart_data_balance = filtered_df.groupby("job")["balance"].mean().sort_values(ascending=False)
        st.bar_chart(chart_data_balance)

    with col_right:
        st.subheader("🎯 Campaign Outcomes by Job")
        # Grouping data to show success distribution across jobs
        if "y" in filtered_df.columns:
            outcome_data = pd.crosstab(filtered_df["job"], filtered_df["y"])
            st.bar_chart(outcome_data)
        else:
            st.info("Outcome column 'y' not found for breakdown.")

    # 6. Data Preview Section
    with st.expander("📂 View Raw Filtered Data Table"):
        st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dataset: {e}. Please ensure 'train.csv' is in your root directory.")