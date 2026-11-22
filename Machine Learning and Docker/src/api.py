from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib
import os

app = FastAPI(title="MNIST Digit Predictor API")

# Load model & scaler
model = joblib.load('models/mnist_model.pkl')
scaler = joblib.load('models/scaler.pkl')

class ImageData(BaseModel):
    pixels: list  

@app.get("/")
def read_root():
    return {"message": "MNIST Digit Predictor API is running. Use POST /predict"}

@app.post("/predict")
def predict_digit(data: ImageData):
    if len(data.pixels) != 784:
        raise HTTPException(status_code=400, detail="Harus 784 pixel")
    
    # Convert to numpy array and scaling
    img_array = np.array(data.pixels, dtype=np.float64).reshape(1, -1)
    img_scaled = scaler.transform(img_array)
    
    # Prediction
    prediction = model.predict(img_scaled)[0]
    proba = model.predict_proba(img_scaled)[0].tolist()
    
    return {
        "predicted_digit": int(prediction),
        "probabilities": proba
    }