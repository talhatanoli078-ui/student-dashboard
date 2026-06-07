import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
page_title="Student Performance Analytics Dashboard",
page_icon="🎓",
layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""

<style>
h1 {
    color: #1E88E5;
}
div[data-testid="metric-container"] {
    border: 1px solid #e6e6e6;
    padding: 10px;
    border-radius: 10px;
}
</style>

""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("StudentsPerformance csv.csv")
# ---------------- TITLE ----------------

st.title("🎓 Student Performance Analytics Dashboard")
st.caption("Interactive dashboard for student performance analysis and visualization")

# ---------------- SIDEBAR ----------------

st.sidebar.header("🔍 Filters")

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

math_range = st.sidebar.slider(
"Math Score Range",
int(df["math score"].min()),
int(df["math score"].max()),
(
int(df["math score"].min()),
int(df["math score"].max())
)
)

st.sidebar.markdown("---")
st.sidebar.info("""
📊 Student Performance Dashboard

Developer: Talha
Built with Streamlit
""")

# ---------------- FILTER DATA ----------------

filtered_df = df[
(df["gender"].isin(gender))
& (df["lunch"].isin(lunch))
& (df["test preparation course"].isin(prep))
& (df["math score"].between(math_range[0], math_range[1]))
]

# ---------------- DOWNLOAD BUTTON ----------------

csv = filtered_df.to_csv(index=False)

st.download_button(
"📥 Download Filtered Data",
csv,
"filtered_students.csv",
"text/csv"
)

# ---------------- KPI CARDS ----------------

st.subheader("📌 KPI Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Students", len(filtered_df))
col2.metric("📘 Math Avg", round(filtered_df["math score"].mean(), 1))
col3.metric("📖 Reading Avg", round(filtered_df["reading score"].mean(), 1))
col4.metric("✍️ Writing Avg", round(filtered_df["writing score"].mean(), 1))

st.divider()

# ---------------- CHARTS ----------------

c1, c2 = st.columns(2)

with c1:
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

with c2:
st.subheader("Gender Distribution")

```
fig, ax = plt.subplots()
counts = filtered_df["gender"].value_counts()

ax.pie(
    counts,
    labels=counts.index,
    autopct="%1.1f%%"
)

st.pyplot(fig)
```

c1, c2 = st.columns(2)

with c1:
st.subheader("Math Score Histogram")

```
fig, ax = plt.subplots()
sns.histplot(
    filtered_df["math score"],
    kde=True,
    ax=ax
)
st.pyplot(fig)
```

with c2:
st.subheader("Test Preparation Count")

```
fig, ax = plt.subplots()
sns.countplot(
    data=filtered_df,
    x="test preparation course",
    ax=ax
)

plt.xticks(rotation=15)
st.pyplot(fig)
```

c1, c2 = st.columns(2)

with c1:
st.subheader("Reading vs Math Score")

```
fig, ax = plt.subplots()

sns.scatterplot(
    data=filtered_df,
    x="math score",
    y="reading score",
    hue="gender",
    ax=ax
)

st.pyplot(fig)
```

with c2:
st.subheader("Writing Score Box Plot")

```
fig, ax = plt.subplots()

sns.boxplot(
    data=filtered_df,
    x="gender",
    y="writing score",
    ax=ax
)

st.pyplot(fig)
```

# ---------------- HEATMAP ----------------

st.subheader("Correlation Heatmap")

corr = filtered_df[
["math score", "reading score", "writing score"]
].corr()

fig, ax = plt.subplots(figsize=(8, 5))

sns.heatmap(
corr,
annot=True,
cmap="coolwarm",
ax=ax
)

st.pyplot(fig)

# ---------------- AREA CHART ----------------

st.subheader("Score Trends")

st.area_chart(
filtered_df[
["math score", "reading score", "writing score"]
]
)

# ---------------- DATASET ----------------

st.subheader("Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("Dataset Statistics")
st.dataframe(filtered_df.describe(), use_container_width=True)

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("© 2026 Student Performance Dashboard | Developed by Talha")
