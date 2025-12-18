from sklearn.model_selection import train_test_split

def split_train_test(df, embeddings, test_size=0.2, random_state=42):
   
    train_indices, test_indices = train_test_split(
        df.index,
        test_size=test_size,
        random_state=random_state,
        stratify=df['label']
    )
    
    df_train = df.loc[train_indices].reset_index(drop=True)
    df_test = df.loc[test_indices].reset_index(drop=True)
    
    embeddings_train = embeddings[train_indices]
    embeddings_test = embeddings[test_indices]
 
    return {
        'df_train': df_train,
        'df_test': df_test,
        'embeddings_train': embeddings_train,
        'embeddings_test': embeddings_test
    }

