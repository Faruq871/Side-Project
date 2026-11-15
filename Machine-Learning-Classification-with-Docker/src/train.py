import numpy as np
import joblib
import os
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, f1_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load MNIST 
X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)
y = y.astype(np.uint8)

# Split
X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
print(f"Train: {X_train.shape}, Test: {X_test.shape}")

# Scaling 
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train.astype(np.float64))
X_test_scaled = scaler.transform(X_test.astype(np.float64))

model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train)

# Evaluasi
y_pred = model.predict(X_test_scaled)
accuracy = np.mean(y_pred == y_test)
f1_macro = f1_score(y_test, y_pred, average='macro')

print(f"\n Accuracy: {accuracy:.4f}")
print(f" F1-Score: {f1_macro:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix - MNIST (Random Forest)')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig('confusion_matrix.png')

# Classification Report (detail per digit)
print("\nCLASSIFICATION")
print(classification_report(y_test, y_pred))

# Simpan model & scaler
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/mnist_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
