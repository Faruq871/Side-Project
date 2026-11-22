import requests
import numpy as np
from sklearn.datasets import fetch_openml

X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
sample_pixels = X[0].tolist()  # ini 784 angka

response = requests.post(
    "http://localhost:8000/predict",
    json={"pixels": sample_pixels}
)

print("Status:", response.status_code)
print("Response:", response.json())