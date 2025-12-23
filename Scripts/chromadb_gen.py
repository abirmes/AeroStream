"""
chromadb_gen.py
Stockage des embeddings dans ChromaDB avec batching
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
import numpy as np


def initialize_chromadb(reset=True, persist_directory="./chroma_db"):

    client = chromadb.PersistentClient(path=persist_directory)
    
    
    if reset:
        try:
            client.delete_collection("airline_train")
            client.delete_collection("airline_test")
        except:
            pass
    return client


def store_embeddings(collection, df, embeddings, batch_size=5000):
  
    total_items = len(df)
    num_batches = (total_items + batch_size - 1) // batch_size
    
    
    for i in range(0, total_items, batch_size):
        end_idx = min(i + batch_size, total_items)
        batch_df = df.iloc[i:end_idx]
        batch_embeddings = embeddings[i:end_idx]
        
        metadatas = []
        for _, row in batch_df.iterrows():
            metadata = {
                "label": int(row['label']),
                "sentiment": row['airline_sentiment']
            }
           
            
            metadatas.append(metadata)
        
        collection.add(
            embeddings=batch_embeddings.tolist(),
            documents=batch_df['text'].tolist(),
            metadatas=metadatas,
            ids=batch_df['id'].tolist()
        )
   


def store_embeddings_train(client, df_train, embeddings_train, batch_size=5000):
   
    collection = client.create_collection(
        name="airline_train",
        metadata={"description": "Training data for airline sentiment"}
    )
    
    store_embeddings(collection, df_train, embeddings_train, batch_size)
    
    return collection


def store_embeddings_test(client, df_test, embeddings_test, batch_size=5000):

    
    collection = client.create_collection(
        name="airline_test",
        metadata={"description": "Test data for airline sentiment"}
    )
    
    store_embeddings(collection, df_test, embeddings_test, batch_size)
    
    return collection

