import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page Config

st.set_page_config(
page_title="Student Performance Dashboard",
page_icon="🎓",
layout="wide"
)

# Load Data

@st.cache_data
@st.cache_data
def load_data():
    return pd.read_csv("StudentsPerformance csv.csv")

df = load_data()
# Title

st.title("🎓 Student Performance Dashboard")
st.write("Analyze student performance using interactive filters and charts.")

# Sidebar Filters

st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
"Gender",
df["gender"].unique(),
default=df["gender"].unique()
)

lunch = st.sidebar.multiselect(
"Lunch Type",
df["lunch"].unique(),
default=df["lunch"].unique()
)

prep = st.sidebar.multiselect(
"Test Preparation",
df["test preparation course"].unique(),
default=df["test preparation course"].unique()
)

# Filter Data

filtered_df = df[
(df["gender"].isin(gender))
& (df["lunch"].isin(lunch))
& (df["test preparation course"].isin(prep))
]

# KPI Cards

col1, col2, col3 = st.columns(3)

col1.metric("Students", len(filtered_df))
col2.metric("Average Math", round(filtered_df["math score"].mean(), 1))
col3.metric("Average Reading", round(filtered_df["reading score"].mean(), 1))

st.divider()

# Charts

col1, col2 = st.columns(2)

with col1:
st.subheader("Average Math Score by Gender")

```
fig, ax = plt.subplots()
sns.barplot(
    data=filtered_df,
    x="gender",
    y="math score",
    estimator="mean",
    ax=ax
)
st.pyplot(fig)
```

with col2:
st.subheader("Gender Distribution")

```
fig, ax = plt.subplots()
filtered_df["gender"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)
ax.set_ylabel("")
st.pyplot(fig)
```

# Histogram

st.subheader("Math Score Distribution")

fig, ax = plt.subplots()
sns.histplot(
filtered_df["math score"],
kde=True,
ax=ax
)
st.pyplot(fig)

# Heatmap

st.subheader("Correlation Heatmap")

corr = filtered_df[
["math score", "reading score", "writing score"]
].corr()

fig, ax = plt.subplots()
sns.heatmap(
corr,
annot=True,
cmap="coolwarm",
ax=ax
)
st.pyplot(fig)

# Dataset Preview

st.subheader("Dataset Preview")
st.dataframe(filtered_df)

# Footer

st.markdown("---")
st.caption("Developed by Talha")
