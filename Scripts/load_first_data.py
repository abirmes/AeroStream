from datasets import load_dataset
import pandas as pd
def load_data(dataset_name="7Xan7der7/us_airline_sentiment"):
    dataset = load_dataset(dataset_name)
    df = pd.DataFrame(dataset['train'])
    return df
