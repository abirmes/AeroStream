import numpy as np
from sentence_transformers import SentenceTransformer

def generate_embeddings(texts, batch_size=64):

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=batch_size
    )
        
    return embeddings
