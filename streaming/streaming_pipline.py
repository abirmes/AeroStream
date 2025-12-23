import requests
import psycopg2
from config import DATABASE_CONFIG, FAKE_API_URL, PREDICTION_API_URL

def create_table():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
            text TEXT,
            airline_sentiment VARCHAR(20),
            airline VARCHAR(50),
            airline_sentiment_confidence FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created")

def stream_batch(batch_size=10):
    tweets = requests.get(f"{FAKE_API_URL}?batch_size={batch_size}").json()
    
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    for tweet in tweets:
        response = requests.post(PREDICTION_API_URL, json={"text": tweet["text"]})
        predicted_sentiment = response.json()["sentiment"]
        
        cur.execute(
            """INSERT INTO predictions (text, airline_sentiment, airline, airline_sentiment_confidence)
               VALUES (%s, %s, %s, %s)""",
            (tweet["text"], predicted_sentiment, tweet["airline"], tweet["airline_sentiment_confidence"])
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print(f" Inserted {batch_size} tweets")

if __name__ == "__main__":
    create_table()
    stream_batch(1)
