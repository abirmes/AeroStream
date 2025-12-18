import pandas as pd
import numpy as np
import os

def save_data(df_train, df_test, embeddings_train, embeddings_test):
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    df_train.to_csv(f'{output_dir}/airline_train.csv', index=False)
    df_test.to_csv(f'{output_dir}/airline_test.csv', index=False)
    
    # Sauvegarde des embeddings
    np.save(f'{output_dir}/embeddings_train.npy', embeddings_train)
    np.save(f'{output_dir}/embeddings_test.npy', embeddings_test)


def load_data(data_dir='data'):
    
    df_train = pd.read_csv(f'{data_dir}/airline_train.csv')
    df_test = pd.read_csv(f'{data_dir}/airline_test.csv')
    embeddings_train = np.load(f'{data_dir}/embeddings_train.npy')
    embeddings_test = np.load(f'{data_dir}/embeddings_test.npy')
    
    
    return {
        'df_train': df_train,
        'df_test': df_test,
        'embeddings_train': embeddings_train,
        'embeddings_test': embeddings_test
    }
