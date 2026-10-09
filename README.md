# 📊 Banking Marketing Campaign Analytics Dashboard

An interactive analytics dashboard built with **Python, Pandas, Plotly, and Streamlit** that turns the public UCI Bank Marketing dataset into an easy-to-explore tool for understanding campaign performance, customer demographics, and the key drivers of term-deposit conversion.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly&logoColor=white)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Key Performance Indicators](#-key-performance-indicators)
- [Exploratory Data Analysis](#-exploratory-data-analysis)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Project Standards](#-project-standards)

---

## 🔎 Overview

This project helps marketing stakeholders answer practical questions about a bank's term-deposit campaigns:

- Which **contact channels** convert best?
- Which **customer segments** (job, age group, education) respond most?
- Does a **previous successful campaign** make a client more likely to subscribe again?
- At what point does **repeated contact** stop paying off?

---

## ✨ Features

| Feature | Description |
|---|---|
| **Dataset integration** | Automatically loads and parses the UCI Bank Marketing dataset (`data/train.csv`) using semicolon delimiters (`sep=";"`). |
| **5 dynamic filters** | Sidebar filters for **Occupation/Job**, **Age Group** (auto-binned from raw age), **Education Level**, **Contact Method**, and **Previous Outcome**. |
| **Live KPI cards** | Filtered Customer Count, Average Account Balance ($), and Campaign Conversion Rate (%). |
| **Interactive visualizations** | Multi-tab panels covering demographic segmentation, job-sector balances, and campaign-specific characteristics. |
| **Raw data explorer** | Expandable table to inspect the underlying filtered data. |

---

## 📈 Key Performance Indicators

### 1. Campaign Response & Conversion Rate
The share of contacted clients who responded positively and subscribed to a term deposit. In this dataset, response and conversion are the same binary target outcome.

```
Conversion Rate = (Clients with y = "yes" / Total Contacted Clients) × 100
```

### 2. Contact Channel Effectiveness
Conversion rate broken down by communication method (e.g., cellular, telephone) to show which channel drives the most engagement.

```
Channel Conversion = (Subscribed Clients per Channel / Total Contacts per Channel) × 100
```

### 3. Segment Targeting Efficiency (Job & Age Group)
Conversion rate across demographic and professional segments to pinpoint high-value customer profiles.

```
Segment Conversion = (Subscribed Clients in Segment / Total Contacts in Segment) × 100
```

---

## 🧪 Exploratory Data Analysis

### Descriptive Statistics

- **Contact methods:** distribution and frequency across cellular, telephone, and unknown channels.
- **Previous campaign outcomes:** historical success, failure, and unknown records, used to gauge retention and retargeting potential.
- **Campaign frequency:** contact attempts per client (`campaign` variable) to track outreach intensity and avoid contact fatigue.

### Visualizations

1. **Conversion Rate by Contact Method**: cellular vs. telephone performance.
2. **Impact of Previous Campaign Outcome**: how past success (`poutcome == 'success'`) relates to current conversion.
3. **Campaign Frequency vs. Conversion**: box plot and distribution of contact attempts against subscriptions.

### Key Findings

- **Past success matters.** Clients with a previously successful campaign subscribe at a dramatically higher rate than cold contacts.
- **Cellular dominates.** Cellular contacts account for most engagement and convert better than landlines.
- **Diminishing returns.** Conversions concentrate in the first 1–4 contact attempts; 10+ attempts show steep drop-off and are operational outliers.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or later
- `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/GP26902/banking-marketing-dashboard.git
cd banking-marketing-dashboard

# Install dependencies
pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

> **Note:** The app reads the dataset from `data/train.csv`, so run the command from the repository root.

---

## 🗂 Project Structure

```
banking-marketing-dashboard/
├── app.py                  # Streamlit dashboard
├── requirements.txt        # Python dependencies
├── README.md
├── data/
│   ├── train.csv           # UCI Bank Marketing dataset (used by the app)
│   └── test.csv
├── docs/
│   ├── task-summaries/     # One summary per completed task
│   └── screenshots/        # Dashboard screenshots
└── notebooks/              # Optional exploratory notebooks
```

---

## ✅ Project Standards

- **Performance:** optimized for load times under 5 seconds.
- **Architecture:** clean, open-source structure.
- **Documentation:** structured, commented code following Python best practices.
- **Version control:** maintained in this GitHub repository.

---

## 📂 Dataset

[UCI Bank Marketing Dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing): data from direct marketing campaigns (phone calls) of a Portuguese banking institution, where the goal is to predict whether a client subscribes to a term deposit.