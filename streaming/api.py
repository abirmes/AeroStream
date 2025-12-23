from fastapi import FastAPI
from pydantic import BaseModel
from model_service import predict_sentiment
import uvicorn

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict(input_data: TextInput):
    sentiment = predict_sentiment(input_data.text)
    return {"text": input_data.text, "sentiment": sentiment}

@app.post("/batch")
def batch(batch_size: int = 10):
    from streaming_pipline import stream_batch
    stream_batch(batch_size)
    return {"status": "ok", "processed": batch_size}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
