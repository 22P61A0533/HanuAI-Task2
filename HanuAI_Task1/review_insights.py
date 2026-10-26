import pandas as pd
from pathlib import Path
from collections import Counter
import re

input_file = Path("reports") / "sentiment_results.xlsx"
output_file = Path("reports") / "review_insights.xlsx"

df = pd.read_excel(input_file)

# Words to ignore when counting frequent words
stop_words = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was",
    "were", "to", "of", "for", "in", "on", "it", "this", "that",
    "with", "my", "i", "me", "they", "them", "you", "your", "we",
    "our", "have", "has", "had", "be", "been", "very", "so",
    "really", "just", "at", "as", "from", "by", "these", "those",
    "its", "it's", "not", "can", "could", "would", "will", "good",
    "great", "nice", "love", "like", "product", "headphones",
    "t", "s", "m", "ll", "re", "ve", "d", "don", "doesn",
    "didn", "wasn", "weren", "isn", "aren", "after", "there",
    "here", "also", "than", "then", "when", "what", "which",
    "who", "how", "if", "about", "up", "out", "off", "into",
    "more", "most", "some", "any", "all", "only", "other",
    "one", "two", "much", "many", "get", "got", "use", "used"
}


def get_common_words(texts):
    words = []

    for text in texts.dropna():
        tokens = re.findall(r"\b[a-zA-Z]+\b", str(text).lower())
        words.extend(
            word for word in tokens
            if word not in stop_words and len(word) > 1
        )

    return Counter(words).most_common(15)


# Group related terms into customer feedback themes.
# These are keyword-based indicators, not verified sentiment judgments.
theme_keywords = {
    "Sound Quality": [
        "sound", "audio", "bass", "treble", "volume", "clarity"
    ],
    "Comfort and Fit": [
        "comfortable", "comfort", "fit", "fitting", "ear", "ears",
        "pressure", "cushion", "cushions"
    ],
    "Noise Cancellation": [
        "anc", "noise cancellation", "cancellation", "canceling",
        "cancelling", "noise cancelling", "noise canceling"
    ],
    "Battery Life": [
        "battery", "battery life", "lasting", "lasts", "hours"
    ],
    "Charging": [
        "charge", "charging", "charged", "charger", "charging port"
    ],
    "Microphone and Calls": [
        "mic", "microphone", "call", "calls", "voice", "receiver"
    ],
    "Build Quality and Durability": [
        "crack", "cracks", "broken", "break", "broke", "durability",
        "defect", "defects", "manufacturing", "joint", "joints",
        "build quality"
    ],
    "Price and Value": [
        "price", "priced", "value", "budget", "cost", "expensive",
        "affordable", "worth"
    ],
    "Appearance and Color": [
        "color", "colour", "attractive", "design", "look", "looks"
    ],
    "Connectivity": [
        "connect", "connecting", "connection", "bluetooth", "pair",
        "pairing", "disconnect", "disconnecting"
    ]
}


def contains_theme(text, keywords):
    text = str(text).lower()

    for keyword in keywords:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            return True

    return False


# Count common words separately for each sentiment
positive_texts = df.loc[
    df["Sentiment"] == "Positive", "Review Text"
]
negative_texts = df.loc[
    df["Sentiment"] == "Negative", "Review Text"
]
neutral_texts = df.loc[
    df["Sentiment"] == "Neutral", "Review Text"
]

positive_words = get_common_words(positive_texts)
negative_words = get_common_words(negative_texts)
neutral_words = get_common_words(neutral_texts)

print("COMMON WORDS IN POSITIVE REVIEWS")
print(positive_words)

print("\nCOMMON WORDS IN NEGATIVE REVIEWS")
print(negative_words)

print("\nCOMMON WORDS IN NEUTRAL REVIEWS")
print(neutral_words)

print("\nSENTIMENT COUNTS")
print(df["Sentiment"].value_counts())


# Count reviews mentioning each theme
theme_results = []

for theme, keywords in theme_keywords.items():
    matching_reviews = df[
        df["Review Text"].apply(
            lambda text: contains_theme(text, keywords)
        )
    ]

    theme_results.append({
        "Customer Theme": theme,
        "Reviews Mentioning Theme": len(matching_reviews),
        "Positive Reviews": int(
            (matching_reviews["Sentiment"] == "Positive").sum()
        ),
        "Negative Reviews": int(
            (matching_reviews["Sentiment"] == "Negative").sum()
        ),
        "Neutral Reviews": int(
            (matching_reviews["Sentiment"] == "Neutral").sum()
        )
    })

themes_df = pd.DataFrame(theme_results)

print("\nCUSTOMER FEEDBACK THEMES")
print(themes_df.to_string(index=False))


# Save all results to an Excel workbook
with pd.ExcelWriter(output_file) as writer:
    df.to_excel(writer, sheet_name="Reviews", index=False)

    pd.DataFrame(
        positive_words, columns=["Word", "Count"]
    ).to_excel(writer, sheet_name="Positive Words", index=False)

    pd.DataFrame(
        negative_words, columns=["Word", "Count"]
    ).to_excel(writer, sheet_name="Negative Words", index=False)

    pd.DataFrame(
        neutral_words, columns=["Word", "Count"]
    ).to_excel(writer, sheet_name="Neutral Words", index=False)

    themes_df.to_excel(
        writer, sheet_name="Customer Themes", index=False
    )

print("\nInsights saved to:", output_file)
