
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="HanuAI ML Assessment",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).parent

st.title("HanuAI — ML Assessment")
st.write("Explore Task 1 and Task 2 from one dashboard.")

page = st.sidebar.radio(
    "Select Assessment",
    [
        "Home",
        "Task 1 — Review Sentiment Analysis",
        "Task 2 — Vehicle Complaint Analysis"
    ]
)


def load_csv(file_paths):
    for file_path in file_paths:
        if file_path.exists():
            try:
                return pd.read_csv(file_path)
            except Exception:
                continue
    return None


if page == "Home":
    st.header("Assessment Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Task 1")
        st.write("Best Buy customer review sentiment analysis.")
        st.write("Explore review data and sentiment results.")

    with col2:
        st.subheader("Task 2")
        st.write("Vehicle complaint analysis.")
        st.write("Explore complaint categories, vehicle makes, tags, and clusters.")

    st.info("Choose a task from the sidebar to view its analysis.")


elif page == "Task 1 — Review Sentiment Analysis":
    st.header("Task 1: Review Sentiment Analysis")

    reviews = load_csv([
        BASE_DIR / "HanuAI_Task1" / "reports" /
        "50_review_sentiment_analysis.csv",

        BASE_DIR / "HanuAI_Task1" / "reports" /
        "bestbuy_reviews_sentiment.csv",

        BASE_DIR / "HanuAI_Task1" / "HanuAI_Task1_Submission" /
        "50_review_sentiment_analysis.csv"
    ])

    if reviews is None:
        st.error(
            "Review data was not found. Check that the Task 1 CSV "
            "files are committed to the GitHub repository."
        )
    else:
        col1, col2 = st.columns(2)
        col1.metric("Total Reviews", len(reviews))
        col2.metric("Total Columns", len(reviews.columns))

        sentiment_columns = [
            col for col in reviews.columns
            if "sentiment" in str(col).lower()
        ]

        if sentiment_columns:
            sentiment_col = sentiment_columns[0]
            counts = (
                reviews[sentiment_col]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
            )

            st.subheader("Sentiment Distribution")
            st.bar_chart(counts)

            st.dataframe(
                counts.rename_axis("Sentiment")
                .reset_index(name="Count"),
                use_container_width=True
            )

        st.subheader("Review Data")
        st.dataframe(reviews.head(50), use_container_width=True)


elif page == "Task 2 — Vehicle Complaint Analysis":
    st.header("Task 2: Vehicle Complaint Analysis")

    complaints = load_csv([
        BASE_DIR / "HanuAI_Task2" / "Hanuai_task2_assignment.csv",
        BASE_DIR / "HanuAI_Task2" / "hanuai_task2_assignment.csv",
        BASE_DIR / "Hanuai_task2_assignment.csv"
    ])

    if complaints is not None:
        col1, col2 = st.columns(2)
        col1.metric("Total Complaints", len(complaints))
        col2.metric("Total Columns", len(complaints.columns))

        category_col = next(
            (c for c in complaints.columns
             if "category" in str(c).lower()),
            None
        )

        make_col = next(
            (c for c in complaints.columns
             if str(c).lower() == "make"),
            None
        )

        if category_col:
            st.subheader("Complaints by Category")
            st.bar_chart(
                complaints[category_col]
                .fillna("Unknown")
                .value_counts()
            )

        if make_col:
            st.subheader("Complaints by Vehicle Make")
            st.bar_chart(
                complaints[make_col]
                .fillna("Unknown")
                .value_counts()
            )

        st.subheader("Complaint Data")
        st.dataframe(complaints.head(50), use_container_width=True)

        st.subheader("Missing Values")
        missing = complaints.isna().sum().sort_values(ascending=False)
        st.dataframe(
            missing.rename_axis("Column")
            .reset_index(name="Missing Values"),
            use_container_width=True
        )

    else:
        st.warning(
            "The original Task 2 dataset was not found. "
            "Checking the saved analysis outputs."
        )

    tags = load_csv([
        BASE_DIR / "HanuAI_Task2" /
        "HanuAI_Task2_Extracted_Tags.csv"
    ])

    clusters = load_csv([
        BASE_DIR / "HanuAI_Task2" /
        "HanuAI_Task2_Cluster_Results.csv"
    ])

    if tags is not None:
        st.subheader("Extracted Complaint Tags")
        st.dataframe(tags.head(100), use_container_width=True)

    if clusters is not None:
        st.subheader("Complaint Clustering Results")
        st.dataframe(clusters.head(100), use_container_width=True)

    st.caption(
        "Complaint counts are not failure rates. Tags and clusters "
        "are exploratory and do not establish confirmed root causes."
    )

st.sidebar.divider()
st.sidebar.caption("HanuAI ML Assessment")
