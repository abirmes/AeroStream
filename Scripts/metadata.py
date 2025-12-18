def prepare_metadata(df):

    df = df.reset_index(drop=True)

    df['id'] = df.index.astype(str)
    
    sentiment_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
    df['label'] = df['airline_sentiment'].map(sentiment_mapping)
    
    return df

