import requests
import psycopg2

# Configuration pour Docker
DATABASE_CONFIG = {
    'host': 'postgres',
    'database': 'aerostream',
    'user': 'postgres',
    'password': 'abir',
    'port': 5432
}

FAKE_API_URL = "http://fake_api:8001/batch"
PREDICTION_API_URL = "http://api:8000/predict"

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

def stream_batch(batch_size=10):
    print(f"Fetching {batch_size} tweets from {FAKE_API_URL}")
    tweets = requests.get(f"{FAKE_API_URL}?batch_size={batch_size}").json()
    
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    for tweet in tweets:
        print(f"Predicting sentiment for: {tweet['text'][:50]}...")
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
