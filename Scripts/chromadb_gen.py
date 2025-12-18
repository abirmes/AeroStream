import chromadb
from chromadb.config import Settings
import pandas as pd

def initialize_chromadb(reset=True):
  
    client = chromadb.Client(Settings(
        anonymized_telemetry=False,
        allow_reset=True
    ))
    
    if reset:
        try:
            client.delete_collection("airline_train")
            client.delete_collection("airline_test")
            print("Collections existantes supprimées")
        except:
            print("Aucune collection existante")
    
    return client


def store_embeddings_train(client, df_train, embeddings_train):
 
    
    collection = client.create_collection(
        name="airline_train",
        metadata={"description": "Training data for airline sentiment"}
    )
    
    collection.add(
        embeddings=embeddings_train.tolist(),
        documents=df_train['text_normalized'].tolist(),
        metadatas=[
            {
                "label": int(label),
                "airline": airline if pd.notna(airline) else "unknown",
                "sentiment": sentiment
            }
            for label, airline, sentiment in zip(
                df_train['label'],
                df_train['airline'] if 'airline' in df_train.columns else ['unknown'] * len(df_train),
                df_train['airline_sentiment']
            )
        ],
        ids=df_train['id'].tolist()
    )
    
    
    return collection


def store_embeddings_test(client, df_test, embeddings_test):
    
    collection = client.create_collection(
        name="airline_test",
        metadata={"description": "Test data for airline sentiment"}
    )
    
    collection.add(
        embeddings=embeddings_test.tolist(),
        documents=df_test['text_normalized'].tolist(),
        metadatas=[
            {
                "label": int(label),
                "airline": airline if pd.notna(airline) else "unknown",
                "sentiment": sentiment
            }
            for label, airline, sentiment in zip(
                df_test['label'],
                df_test['airline'] if 'airline' in df_test.columns else ['unknown'] * len(df_test),
                df_test['airline_sentiment']
            )
        ],
        ids=df_test['id'].tolist()
    )
    
    
    return collection
