"""
Author : Aman Ulla (connectamanulla@gmail.com)
This Scrpt We Assume we are using Logistic Regression Model
and use Refit technique to update the weights on the incremental data

NOTE: The model is newly initiated, if not found in local directory
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib
import os

class ModelTrainer:
    def __init__(self, initial_data_size=1000, num_features=12, model_path='models/logistic_model.pkl'):
        self.model = None
        self.initial_data_size = initial_data_size
        self.num_features = num_features
        self.model_path = model_path
        self._ensure_model_directory()
        self._load_model()

    def _ensure_model_directory(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

    def _generate_data(self, num_samples):
        X = np.random.rand(num_samples, self.num_features)
        y = np.random.randint(0, 2, size=num_samples)
        return X, y

    def _train_initial_model(self):
        X_train, y_train = self._generate_data(self.initial_data_size)
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)
        print("Initial model trained.")

    def _load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}.")
        else:
            self._train_initial_model()

    def save_model(self):
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}.")

    def fine_tune(self, X_new, y_new):
        self.model.fit(X_new, y_new)
        print("Model fine-tuned with new data.")

    def get_model(self):
        return self.model
