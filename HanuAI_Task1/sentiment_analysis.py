
import pandas as pd
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# File paths
input_file = Path("data") / "hanuaI_reviews.xlsx"
output_file = Path("reports") / "sentiment_results.xlsx"

# Load reviews
df = pd.read_excel(input_file)

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze each review
def analyze_sentiment(text):
    scores = analyzer.polarity_scores(str(text))
    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return pd.Series({
        "Sentiment": label,
        "Sentiment Score": compound
    })

# Apply sentiment analysis to review text
df[["Sentiment", "Sentiment Score"]] = df["Review Text"].apply(
    analyze_sentiment
)

# Create output folder if it doesn't exist
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save results separately
df.to_excel(output_file, index=False)

# Display summary
print("Sentiment analysis completed!")
print("\nSentiment counts:")
print(df["Sentiment"].value_counts())

print("\nResults saved to:", output_file)
print("\nFirst 5 results:")
print(df[["Review title", "Sentiment", "Sentiment Score"]].head())
