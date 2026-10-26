
import pandas as pd
from pathlib import Path

file_path = Path("data") / "hanuaI_reviews.xlsx"

df = pd.read_excel(file_path)

print("Total reviews:", len(df))

# Check duplicate IDs
print("\nDuplicate IDs:", df["ID"].duplicated().sum())

# Check invalid ratings
ratings = pd.to_numeric(df["Rating"], errors="coerce")
invalid_ratings = ratings.isna() | ~ratings.between(1, 5)
print("Invalid or missing ratings:", invalid_ratings.sum())

# Check date format
dates = pd.to_datetime(df["Date"], errors="coerce")
invalid_dates = dates.isna()
print("Invalid or missing dates:", invalid_dates.sum())

# Check empty review text
empty_reviews = df["Review Text"].isna() | (
    df["Review Text"].astype(str).str.strip() == ""
)
print("Empty review texts:", empty_reviews.sum())

# Check duplicate review text
print(
    "Duplicate review texts:",
    df["Review Text"].astype(str).str.strip().duplicated().sum()
)

print("\nValidation complete.")
