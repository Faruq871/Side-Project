# MNIST Digit Classifier API with FastAPI and Docker

A production-ready **MNIST digit classification API** built with **FastAPI**, **scikit-learn**, and containerized with **Docker**. This project demonstrates a complete MLOps pipeline: model training, API development, and containerization.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Training the Model](#training-the-model)
- [Running the API Locally](#running-the-api-locally)
- [Testing the API](#testing-the-api)
- [Running with Docker](#running-with-docker)
- [Project Structure](#project-structure)
- [License](#license)

---

## 🧠 Overview

This project implements a **Random Forest classifier** trained on the MNIST dataset (70,000 handwritten digits). The trained model is exposed via a **RESTful API** built with FastAPI, allowing users to send image pixel data (784 integers) and receive digit predictions with confidence scores.

The entire application can be run locally or inside a **Docker container**, making it portable and easy to deploy.

---

## ✨ Features

- ✅ **Multi-class classification** (digits 0–9) with ~97% accuracy  
- ✅ **FastAPI** endpoints with automatic interactive documentation (`/docs`)  
- ✅ **Input validation** (expects exactly 784 pixel values)  
- ✅ **Probability scores** for each class in the response  
- ✅ **Dockerized** for consistent deployment across environments  
- ✅ **Scaler serialization** – preprocessing pipeline saved and reloaded  

---

## 🛠️ Tech Stack

| Component          | Technology                          |
|--------------------|-------------------------------------|
| **Machine Learning** | scikit-learn (Random Forest)       |
| **API Framework**    | FastAPI                            |
| **Server**           | Uvicorn                            |
| **Containerization** | Docker                             |
| **Data Handling**    | NumPy, joblib                      |
| **Validation**       | Pydantic                           |
| **Testing**          | requests, fetch_openml             |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+**
- **pip** (Python package manager)
- **Docker** (optional, for containerized deployment)

---

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Faruq871/Machine-Learning---Classification-with-Docker-
   cd Machine-Learning---Classification-with-Docker-
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏋️ Training the Model

Run the training script to download MNIST, train the Random Forest classifier, and save the model + scaler.

```bash
py src/train.py
```

**Expected output:**
```
✅ Accuracy: 0.9704
✅ F1-Score (macro): 0.9701
📊 Confusion Matrix saved as 'confusion_matrix.png'
💾 Model saved to 'models/mnist_model.pkl'
💾 Scaler saved to 'models/scaler.pkl'
```

> **Note:** The model file (`mnist_model.pkl`) is ~137 MB and is **not** included in the repository. It is generated locally during training and ignored by Git.

---

## 🚀 Running the API Locally

Start the FastAPI server with Uvicorn:

```bash
uvicorn src.api:app --reload
```

The API will be available at:  
👉 **http://localhost:8000**

Interactive API documentation (Swagger UI) is available at:  
👉 **http://localhost:8000/docs**

---

## 🧪 Testing the API

You can test the API using the provided test script:

```bash
py src/main.py
```

**Expected response:**
```json
{
  "Status": 200,
  "Response": {
    "predicted_digit": 5,
    "probabilities": [0.0, 0.0, 0.01, 0.08, 0.0, 0.9, 0.0, 0.0, 0.0, 0.01]
  }
}
```

**Or use `curl`**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"pixels": [0,0,0,...,0]}'   # Replace with 784 integers
```

---

## 🐳 Running with Docker

### 1️⃣ Build the Docker image
```bash
docker build -t mnist-api .
```

### 2️⃣ Run the container
```bash
docker run -p 8000:8000 mnist-api
```

### 3️⃣ Test inside the container
Open another terminal and run:
```bash
py src/main.py
```

You should see the same `Status: 200` response, confirming the API is working inside the container.

---

## 📁 Project Structure

```
proyek_ml/
├── models/                     # Saved model and scaler (ignored by Git)
│   ├── mnist_model.pkl
│   └── scaler.pkl
├── src/
│   ├── api.py                  # FastAPI app
│   ├── main.py                 # Test client
│   └── train.py                # Training script
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── .gitignore                  # Ignored files
├── confusion_matrix.png        # Confusion matrix visualization
└── README.md                   # This file
```

---

## 📄 License

This project is for educational purposes. Feel free to use and modify it.

---

## 👨‍💻 Author

**Faruq**  
GitHub: [@Faruq871](https://github.com/Faruq871)

---

## 🙌 Acknowledgments

- [MNIST dataset](http://yann.lecun.com/exdb/mnist/) – Yann LeCun, Corinna Cortes, Christopher J.C. Burges  
- Built with guidance from Aurélien Géron's *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow*
