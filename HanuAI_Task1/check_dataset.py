
import pandas as pd
from pathlib import Path

file_path = Path("data") / "hanuaI_reviews.xlsx"

if not file_path.exists():
    print("Excel file not found. Check the filename and data folder.")
else:
    df = pd.read_excel(file_path)

    print("Number of reviews:", len(df))
    print("\nColumn names:")
    print(list(df.columns))

    print("\nFirst 5 reviews:")
    print(df.head())

    print("\nMissing values in each column:")
    print(df.isnull().sum())

    print("\nDataset inspection complete.")
