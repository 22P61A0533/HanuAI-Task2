
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="HanuAI Task 1 - Review Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("HanuAI — Task 1")
st.subheader("Best Buy Customer Review Sentiment Analysis")

BASE = Path(__file__).parent
REPORTS = BASE / "reports"

st.write(
    "Explore the review sentiment results and business insights "
    "generated for Task 1."
)

sentiment_file = REPORTS / "50_review_sentiment_analysis.csv"
full_file = REPORTS / "bestbuy_reviews_sentiment.csv"

selected_file = (
    sentiment_file if sentiment_file.exists()
    else full_file if full_file.exists()
    else None
)

if selected_file is None:
    st.error("Sentiment CSV file not found in HanuAI_Task1/reports.")
    st.stop()

@st.cache_data
def load_reviews(path):
    return pd.read_csv(path)

df = load_reviews(str(selected_file))

st.subheader("Review dataset overview")
c1, c2 = st.columns(2)
c1.metric("Reviews", len(df))
c2.metric("Columns", len(df.columns))

st.subheader("Review data preview")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("Available columns")
st.write(", ".join(map(str, df.columns)))

sentiment_columns = [
    col for col in df.columns
    if "sentiment" in col.lower()
]

if sentiment_columns:
    sentiment_col = sentiment_columns[0]
    st.subheader("Sentiment distribution")
    counts = (
        df[sentiment_col]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
    )
    st.bar_chart(counts)

    st.dataframe(
        counts.rename_axis("Sentiment").reset_index(name="Count"),
        use_container_width=True
    )
else:
    st.info(
        "A sentiment column was not detected automatically. "
        "Review the available columns above."
    )

with st.expander("Task 1 report files"):
    if REPORTS.exists():
        for file in sorted(REPORTS.iterdir()):
            if file.is_file():
                st.write(file.name)

st.info(
    "Sentiment labels and business insights should be interpreted "
    "within the scope and limitations of the available review data."
)
