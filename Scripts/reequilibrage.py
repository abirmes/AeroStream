

import pandas as pd
import nlpaug.augmenter.word as naw
import nltk
from collections import Counter

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)


def reequilibrer_donnees(df):

    aug = naw.SynonymAug(aug_src='wordnet')
    
    class_counts = Counter(df['airline_sentiment'])
    max_count = max(class_counts.values())
    

    nouvelles_lignes = []
    
    for sentiment, count in class_counts.items():
        
        if count < max_count:
            difference = max_count - count
            
            subset = df[df['airline_sentiment'] == sentiment]
            
            for i in range(difference):
                ligne_originale = subset.iloc[i % len(subset)]
                
                texte_augmente = aug.augment(ligne_originale['text'])
                
                nouvelle_ligne = ligne_originale.copy()
                nouvelle_ligne['text'] = texte_augmente
                
                nouvelles_lignes.append(nouvelle_ligne)
    
    df_augmente = pd.DataFrame(nouvelles_lignes)
    
    df = pd.concat([df, df_augmente], ignore_index=True)
    

    print(f"Taille avant:  {len(df)} lignes")
    print(f"Taille après:  {len(df)} lignes")
    print(f"Ajoutées:      {len(df_augmente)} lignes")
    
    print(df['airline_sentiment'].value_counts())
    
    return df

