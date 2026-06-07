```python
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Student Performance Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}
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
@st.cache_data
def load_data():
    return pd.read_csv("StudentsPerformance csv.csv")

df = load_data()

# ---------------- TITLE ----------------
st.title("🎓 Student Performance Analytics Dashboard")
st.markdown(
    "Interactive dashboard for analyzing student performance, demographics, and academic trends."
)

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
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_students.csv",
    mime="text/csv"
)

# ---------------- KPI CARDS ----------------
st.subheader("📌 KPI Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Total Students", len(filtered_df))
col2.metric("📘 Avg Math", round(filtered_df["math score"].mean(), 2))
col3.metric("📖 Avg Reading", round(filtered_df["reading score"].mean(), 2))
col4.metric("✍️ Avg Writing", round(filtered_df["writing score"].mean(), 2))

st.divider()

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(
    ["📊 Overview", "📈 Advanced Analysis", "📋 Dataset"]
)

# ================= TAB 1 =================
with tab1:

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Average Math Score by Gender")

        fig, ax = plt.subplots()
        sns.barplot(
            data=filtered_df,
            x="gender",
            y="math score",
            estimator="mean",
            ax=ax
        )
        st.pyplot(fig)

    with c2:
        st.subheader("Gender Distribution")

        fig, ax = plt.subplots()
        counts = filtered_df["gender"].value_counts()

        ax.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

    st.subheader("Interactive Scatter Plot")

    fig = px.scatter(
        filtered_df,
        x="math score",
        y="reading score",
        color="gender",
        hover_data=["writing score"]
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 2 =================
with tab2:

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Histogram")

        fig, ax = plt.subplots()

        sns.histplot(
            filtered_df["math score"],
            kde=True,
            ax=ax
        )

        st.pyplot(fig)

    with c2:
        st.subheader("Count Plot")

        fig, ax = plt.subplots()

        sns.countplot(
            data=filtered_df,
            x="test preparation course",
            ax=ax
        )

        plt.xticks(rotation=15)

        st.pyplot(fig)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Box Plot")

        fig, ax = plt.subplots()

        sns.boxplot(
            data=filtered_df,
            x="gender",
            y="writing score",
            ax=ax
        )

        st.pyplot(fig)

    with c4:
        st.subheader("Violin Plot")

        fig, ax = plt.subplots()

        sns.violinplot(
            data=filtered_df,
            x="gender",
            y="math score",
            ax=ax
        )

        st.pyplot(fig)

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

    st.subheader("Area Chart")

    st.area_chart(
        filtered_df[
            ["math score", "reading score", "writing score"]
        ]
    )

# ================= TAB 3 =================
with tab3:

    st.subheader("Dataset Preview")
    st.dataframe(filtered_df)

    st.subheader("Dataset Statistics")
    st.write(filtered_df.describe())

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "© 2026 Student Performance Analytics Dashboard | Built with Streamlit"
)
```
