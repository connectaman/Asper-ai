from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List
from pydantic import BaseModel
import numpy as np
import threading
import os

from src.train import ModelTrainer

app = FastAPI()
trainer = ModelTrainer()
batch_storage = []
fine_tuning_active = False

class BatchData(BaseModel):
    X: List[List[float]]
    y: List[int]

class MessageResponse(BaseModel):
    message: str

def fine_tune_worker():
    global fine_tuning_active
    while fine_tuning_active:
        if batch_storage:
            X, y = batch_storage.pop(0)
            trainer.fine_tune(X, y)
            trainer.save_model()
            print("Model fine-tuned with batch data.")
        else:
            threading.Event().wait(1)  # Sleep briefly if no batches are available

@app.on_event("startup")
async def on_startup():
    global fine_tuning_active
    fine_tuning_active = True
    trainer._load_model()
    print("Model training triggered on startup.")

@app.post("/fine-tune", response_model=MessageResponse)
async def fine_tune(data: BatchData, background_tasks: BackgroundTasks):
    global fine_tuning_active
    X = np.array(data.X)
    y = np.array(data.y)

    if not fine_tuning_active:
        fine_tuning_active = True
        background_tasks.add_task(fine_tune_worker)

    batch_storage.append((X, y))
    return MessageResponse(message="Fine-tuning triggered")

@app.get("/model", response_model=MessageResponse)
async def get_model_status():
    if trainer.get_model():
        return MessageResponse(message="Model is ready and fine-tuning is active.")
    else:
        raise HTTPException(status_code=404, detail="Model not initialized yet.")

@app.post("/shutdown", response_model=MessageResponse)
async def shutdown():
    global fine_tuning_active
    fine_tuning_active = False
    trainer.save_model()
    return MessageResponse(message="Service shutting down and model saved.")