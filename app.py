import pandas as pd
import plotly.express as px
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

PLOT_TEMPLATE = "plotly_dark"


# 2. Load Dataset
@st.cache_data
def load_banking_data():
    df = pd.read_csv("data/train.csv", sep=";")

    # Preprocess Age into Age Groups to satisfy age filtering requirements
    if "age" in df.columns:
        bins = [0, 25, 35, 50, 65, 120]
        labels = ["<25", "25-35", "36-50", "51-65", "65+"]
        df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)

    return df


def summarize_by(data, group_col, success_col):
    """Count, share of contacts, conversions and conversion rate for each category."""
    grouped = data.groupby(group_col, observed=True)
    summary = grouped.size().rename("Contacts").to_frame()
    summary["% of Contacts"] = (summary["Contacts"] / summary["Contacts"].sum() * 100).round(2)
    if success_col:
        summary["Conversions"] = grouped["converted"].sum().astype(int)
        summary["Conversion Rate (%)"] = (summary["Conversions"] / summary["Contacts"] * 100).round(2)
    return summary.sort_values("Contacts", ascending=False)


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

    # Binary conversion flag used by the campaign EDA tab
    if success_col:
        filtered_df = filtered_df.copy()
        filtered_df["converted"] = (
            filtered_df[success_col].astype(str).str.lower().isin(["yes", "1", "true"]).astype(int)
        )

    # 5. Tabbed Layout
    tab_demo, tab_campaign = st.tabs(["👥 Demographics & Balances", "📞 Campaign Characteristics (EDA)"])

    # ------------------------------------------------------------------
    # TAB 1: Existing visualizations (unchanged)
    # ------------------------------------------------------------------
    with tab_demo:
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

    # ------------------------------------------------------------------
    # TAB 2: Exploratory Data Analysis on campaign characteristics
    # ------------------------------------------------------------------
    with tab_campaign:
        st.markdown(
            "Exploratory analysis of **contact method**, **campaign frequency** and "
            "**previous campaign outcome**. All results respond to the sidebar filters."
        )

        if total_customers == 0:
            st.warning("No records match the current filters. Adjust the sidebar filters to see the analysis.")
        else:
            # ---- A. Descriptive statistics -----------------------------
            st.subheader("📋 Descriptive Statistics")

            stat_left, stat_right = st.columns(2)

            with stat_left:
                st.markdown("**Contact Method**")
                if "contact" in filtered_df.columns:
                    st.dataframe(summarize_by(filtered_df, "contact", success_col), use_container_width=True)
                else:
                    st.info("'contact' column unavailable.")

            with stat_right:
                st.markdown("**Previous Campaign Outcome**")
                if "poutcome" in filtered_df.columns:
                    st.dataframe(summarize_by(filtered_df, "poutcome", success_col), use_container_width=True)
                else:
                    st.info("'poutcome' column unavailable.")

            st.markdown("**Campaign Frequency & Prior Contact (numeric summary)**")
            numeric_cols = [c for c in ["campaign", "previous", "pdays"] if c in filtered_df.columns]
            if numeric_cols:
                st.dataframe(filtered_df[numeric_cols].describe().T.round(2), use_container_width=True)
                if "pdays" in numeric_cols:
                    st.caption("Note: in this dataset, `pdays = -1` means the client was not previously contacted.")
            else:
                st.info("Numeric campaign columns unavailable.")

            st.divider()

            # ---- B. Visualizations -------------------------------------
            st.subheader("📈 Campaign Visualizations")

            viz1, viz2 = st.columns(2)

            # Visualization 1: Conversion rate by contact method
            with viz1:
                st.markdown("**1. Conversion Rate by Contact Method**")
                if "contact" in filtered_df.columns and success_col:
                    contact_summary = summarize_by(filtered_df, "contact", success_col).reset_index()
                    fig_contact = px.bar(
                        contact_summary,
                        x="contact",
                        y="Conversion Rate (%)",
                        color="contact",
                        text="Conversion Rate (%)",
                        hover_data=["Contacts", "Conversions"],
                        template=PLOT_TEMPLATE,
                    )
                    fig_contact.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
                    fig_contact.update_layout(showlegend=False, xaxis_title="Contact Method")
                    st.plotly_chart(fig_contact, use_container_width=True)
                else:
                    st.info("Contact method or outcome column unavailable.")

            # Visualization 2: Impact of previous campaign outcome
            with viz2:
                st.markdown("**2. Impact of Previous Campaign Outcome**")
                if "poutcome" in filtered_df.columns and success_col:
                    pout_summary = summarize_by(filtered_df, "poutcome", success_col).reset_index()
                    fig_pout = px.bar(
                        pout_summary,
                        x="poutcome",
                        y="Conversion Rate (%)",
                        color="poutcome",
                        text="Conversion Rate (%)",
                        hover_data=["Contacts", "Conversions"],
                        template=PLOT_TEMPLATE,
                    )
                    fig_pout.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
                    fig_pout.update_layout(showlegend=False, xaxis_title="Previous Outcome")
                    st.plotly_chart(fig_pout, use_container_width=True)
                else:
                    st.info("Previous outcome or outcome column unavailable.")

            viz3, viz4 = st.columns(2)

            # Visualization 3a: Campaign frequency distribution by outcome (box plot)
            with viz3:
                st.markdown("**3a. Campaign Frequency vs. Subscription (Box Plot)**")
                if "campaign" in filtered_df.columns and success_col:
                    fig_box = px.box(
                        filtered_df,
                        x=success_col,
                        y="campaign",
                        color=success_col,
                        points="outliers",
                        template=PLOT_TEMPLATE,
                    )
                    fig_box.update_layout(
                        showlegend=False,
                        xaxis_title="Subscribed to Term Deposit",
                        yaxis_title="Contact Attempts (campaign)",
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                else:
                    st.info("Campaign frequency or outcome column unavailable.")

            # Visualization 3b: Conversion rate by number of contact attempts
            with viz4:
                st.markdown("**3b. Conversion Rate by Number of Contact Attempts**")
                if "campaign" in filtered_df.columns and success_col:
                    attempts = filtered_df.copy()
                    attempts["attempt_bucket"] = pd.cut(
                        attempts["campaign"],
                        bins=[0, 1, 2, 3, 4, 10, float("inf")],
                        labels=["1", "2", "3", "4", "5-10", "11+"],
                    )
                    bucket_summary = (
                        attempts.groupby("attempt_bucket", observed=True)
                        .agg(Contacts=("converted", "size"), Conversions=("converted", "sum"))
                        .reset_index()
                    )
                    bucket_summary["Conversion Rate (%)"] = (
                        bucket_summary["Conversions"] / bucket_summary["Contacts"] * 100
                    ).round(2)
                    fig_attempts = px.line(
                        bucket_summary,
                        x="attempt_bucket",
                        y="Conversion Rate (%)",
                        markers=True,
                        hover_data=["Contacts", "Conversions"],
                        template=PLOT_TEMPLATE,
                    )
                    fig_attempts.update_layout(xaxis_title="Contact Attempts", yaxis_title="Conversion Rate (%)")
                    st.plotly_chart(fig_attempts, use_container_width=True)
                else:
                    st.info("Campaign frequency or outcome column unavailable.")

            st.divider()

            # ---- C. Notable patterns & outliers ------------------------
            st.subheader("🔎 Notable Patterns & Outliers")
            st.caption("Generated automatically from the currently filtered data.")

            insights = []

            # Dominant contact channel
            if "contact" in filtered_df.columns:
                channel_counts = filtered_df["contact"].value_counts()
                top_channel = channel_counts.index[0]
                top_share = channel_counts.iloc[0] / total_customers * 100
                msg = f"**Channel dominance:** `{top_channel}` is the most used contact method, covering {top_share:.1f}% of contacts"
                if success_col:
                    channel_rates = filtered_df.groupby("contact")["converted"].mean() * 100
                    best_channel = channel_rates.idxmax()
                    msg += f". The highest conversion rate belongs to `{best_channel}` at {channel_rates.max():.2f}%."
                else:
                    msg += "."
                insights.append(msg)

            # Previous outcome effect
            if "poutcome" in filtered_df.columns and success_col:
                pout_rates = filtered_df.groupby("poutcome")["converted"].agg(["mean", "size"])
                if "success" in pout_rates.index:
                    success_rate_prev = pout_rates.loc["success", "mean"] * 100
                    others = filtered_df[filtered_df["poutcome"] != "success"]
                    if len(others) > 0:
                        other_rate = others["converted"].mean() * 100
                        insights.append(
                            f"**Past success matters:** clients with a previously successful campaign convert at "
                            f"{success_rate_prev:.2f}%, versus {other_rate:.2f}% for all other clients."
                        )

            # Campaign frequency: concentration and diminishing returns
            if "campaign" in filtered_df.columns and success_col:
                converted_df = filtered_df[filtered_df["converted"] == 1]
                if len(converted_df) > 0:
                    early_share = (converted_df["campaign"] <= 4).mean() * 100
                    insights.append(
                        f"**Early conversions:** {early_share:.1f}% of all subscriptions happened within the first 4 contact attempts."
                    )

                heavy = filtered_df[filtered_df["campaign"] > 10]
                light = filtered_df[filtered_df["campaign"] <= 4]
                if len(heavy) > 0 and len(light) > 0:
                    insights.append(
                        f"**Diminishing returns:** clients contacted more than 10 times convert at "
                        f"{heavy['converted'].mean() * 100:.2f}%, compared with {light['converted'].mean() * 100:.2f}% "
                        f"for clients contacted 1-4 times ({len(heavy):,} clients are in the 10+ group)."
                    )

            # Outlier detection on campaign frequency (IQR rule)
            if "campaign" in filtered_df.columns:
                q1 = filtered_df["campaign"].quantile(0.25)
                q3 = filtered_df["campaign"].quantile(0.75)
                upper_fence = q3 + 1.5 * (q3 - q1)
                outliers = filtered_df[filtered_df["campaign"] > upper_fence]
                insights.append(
                    f"**Outliers:** using the IQR rule, any client contacted more than {upper_fence:.0f} times is an outlier. "
                    f"That is {len(outliers):,} clients ({len(outliers) / total_customers * 100:.2f}%), "
                    f"with a maximum of {int(filtered_df['campaign'].max())} attempts for a single client."
                )

            for item in insights:
                st.markdown(f"- {item}")

    # 6. Data Preview Section
    with st.expander("📂 View Raw Filtered Data Table"):
        st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading or processing dataset: {e}. Please ensure 'train.csv' is in your root directory.")