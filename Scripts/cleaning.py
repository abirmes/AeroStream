import re
def clean_text(text) :
    text = re.sub(r"(https?://\S+|www\.\S+)", "", text)
    text = re.sub(r"[\U00010000-\U0010ffff]", "", text)
    text = re.sub(r"[^\w\s.,!?'-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

def clean_dataframe(df):
    cols = [
    "airline_sentiment",
    "airline_sentiment_confidence",
    "airline",
    "text",
]

    df = df[cols]
    df_cleaned = df.drop_duplicates()
    
    df_cleaned = df_cleaned.dropna(subset=['text'])
    
    df_cleaned['text'] = df_cleaned['text'].apply(clean_text)
    
    
    return df_cleaned
