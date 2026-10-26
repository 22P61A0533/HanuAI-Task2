
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="HanuAI | Vehicle Complaint Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("HanuAI — Vehicle Complaint Analysis")
st.caption("ML Assessment | Exploratory Data Analysis and Text Mining")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "HanuAI_Task2"

@st.cache_data
def load_data():
    candidates = [
        DATA_DIR / "Hanuai_task2_assignment.csv",
        BASE_DIR / "Hanuai_task2_assignment.csv",
    ]
    for path in candidates:
        if path.exists():
            return pd.read_csv(path)
    return None

df = load_data()

if df is None:
    st.error(
        "Dataset CSV not found. Check that "
        "Hanuai_task2_assignment.csv is included in "
        "the repository in the HanuAI_Task2 folder."
    )
    st.stop()

st.subheader("Dataset overview")
c1, c2 = st.columns(2)
c1.metric("Total complaint records", f"{len(df):,}")
c2.metric("Total columns", len(df.columns))

with st.expander("Preview dataset"):
    st.dataframe(df.head(20), use_container_width=True)

if "COMPLAINT_CD_DESC" in df.columns:
    st.subheader("Complaints by category")
    category_counts = (
        df["COMPLAINT_CD_DESC"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Complaint category")
        .reset_index(name="Count")
    )
    st.bar_chart(
        category_counts.set_index("Complaint category")
    )
    st.dataframe(category_counts, use_container_width=True)

if "MAKE" in df.columns:
    st.subheader("Complaints by vehicle make")
    make_counts = (
        df["MAKE"]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Vehicle make")
        .reset_index(name="Count")
    )
    st.bar_chart(make_counts.set_index("Vehicle make"))

if "Opened date" in df.columns:
    st.subheader("Complaints over time")
    dates = pd.to_datetime(df["Opened date"], errors="coerce")
    monthly = (
        dates.dropna()
        .dt.to_period("M")
        .value_counts()
        .sort_index()
    )
    if not monthly.empty:
        monthly.index = monthly.index.astype(str)
        st.line_chart(monthly.rename("Complaints"))

st.subheader("Data quality")
missing = (
    df.isna().sum()
    .rename("Missing values")
    .to_frame()
)
st.dataframe(missing, use_container_width=True)

st.info(
    "These visualizations describe complaint records, not "
    "vehicle failure rates. The dataset does not provide "
    "production-volume denominators. Text tags and clusters "
    "are exploratory indicators, not verified root causes."
)

st.caption("HanuAI ML Assessment — Task 2")
