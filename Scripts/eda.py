import pandas as pd

def perform_eda(df):
 
    stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'sentiment_distribution': df['airline_sentiment'].value_counts().to_dict(),
        'missing_values': df.isnull().sum().to_dict()
    }
    
    if 'airline' in df.columns:
        stats['airline_distribution'] = df['airline'].value_counts().to_dict()
    
    print(f"Lignes: {stats['total_rows']}")
    print(f"Colonnes: {stats['total_columns']}")
    print(f"Distribution sentiments: {stats['sentiment_distribution']}")
    
    return stats


