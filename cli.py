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
import time

from src.train import ModelTrainer

def main():
    trainer = ModelTrainer()

    # Simulate streaming data and fine-tune the model
    try:
        while True:
            X_batch, y_batch = trainer._generate_data(10)
            print(f"Received batch data with shape X: {X_batch.shape}, y: {y_batch.shape}")
            trainer.fine_tune(X_batch, y_batch)
            trainer.save_model()
            time.sleep(3)
    except KeyboardInterrupt:
        print("Training interrupted by user. Exiting...")
        trainer.save_model()

if __name__ == "__main__":
    main()

