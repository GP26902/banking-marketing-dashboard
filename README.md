# Task Summary: Banking Marketing Campaign Analytics Dashboard

**Project:** Banking Marketing Campaign Analytics Dashboard  
**Repository Link:**  https://github.com/GP26902/banking-marketing-dashboard

## 1. Executive Summary

As part of our open-source initiative, we have developed a fully functional, interactive analytics dashboard using Python, Pandas, and Streamlit. The dashboard transforms the public banking marketing dataset into an accessible tool for exploring campaign performance, evaluating customer demographics, and identifying key conversion drivers, directly fulfilling the project’s PRD and Charter guidelines.


## 2. Key Performance Indicators (KPIs)

To rigorously evaluate marketing campaign performance, the project formally tracks the following core metrics:

* **Overall Conversion Rate**
  - **Definition:** The proportion of total contacted clients who successfully subscribed to a term deposit.
  - **Formula:** $(\text{Total Subscribed Clients} / \text{Total Contacted Clients}) \times 100$
  - **Measurability:** Calculated directly from the target outcome column divided by the total row count in the dataset.

* **Contact Channel Effectiveness**
  - **Definition:** The conversion rate broken down by the specific communication method used (e.g., cellular, telephone) to identify which channel drives the highest engagement.
  - **Formula:** $(\text{Subscribed Clients per Channel} / \text{Total Contacts per Channel}) \times 100$
  - **Measurability:** Derived by grouping the dataset by the contact method feature and computing the subscription ratio for each group.

* **Segment Targeting Efficiency (Job & Age Group)**
  - **Definition:** The response and conversion rate across distinct demographic and professional segments to pinpoint high-value customer profiles.
  - **Formula:** $(\text{Subscribed Clients within a Specific Segment} / \text{Total Contacts in That Segment}) \times 100$
  - **Measurability:** Calculated by applying the demographic categorical filters (`Job`, `Age Group`) against the conversion outcome.


## 3. Implementation & Key Features

The dashboard has been successfully architected and deployed to the GitHub repository with the following core components:
* **Dataset Integration (FR1):** Automatically loads and parses the UCI Bank Marketing dataset (`train.csv`) using proper semicolon delineation (`sep=";"`).
* **5 Distinct Characteristic Filters (FR3):** Implements dynamic sidebar filters across five key customer and campaign dimensions:
  - Occupation / Job
  - Age Group (automatically binned from raw age data)
  - Education Level
  - Contact Method
  - Previous Outcome
* **Key Performance Indicators (FR2):** Real-time metric cards displaying Filtered Customer Count, Average Account Balance ($), and Campaign Success / Conversion Rate (%).
* **Interactive Visualizations (FR4 & FR5):** Side-by-side analytical panels showing average balances by job sector and campaign outcome distributions across customer segments.
* **Raw Data Explorer:** An expandable data table allowing stakeholders to inspect the underlying filtered dataset.


## 4. Compliance & Standards

* **Non-Functional Requirements (NFR1–NFR5):** Optimized for performance (<5 second load times), designed with a clean open-source architecture, and fully documented.
* **Code Maintenance:** The code is structured, commented following Python best practices, and stored in our version-controlled GitHub repository.


## 5. How to Run Locally

To run the dashboard locally for testing or review:

1. Ensure Python, Streamlit, and Pandas are installed (`pip install streamlit pandas`).
2. Place `train.csv` in the root directory alongside `app.py`.
3. Run the following command in your terminal:
   ```bash
   streamlit run app.py