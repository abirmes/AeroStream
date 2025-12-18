def normalize_text(df):
   
    df['text'] = df['text'].str.lower()
    return df
