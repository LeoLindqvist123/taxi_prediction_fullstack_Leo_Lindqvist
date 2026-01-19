from fastapi import FastAPI, APIRouter
import pandas as pd
import joblib
from constants import DATA_PATH, MODELS_PATH, FEATURES_PATH
from pydantic import BaseModel, Field

df = pd.read_csv(DATA_PATH / "taxi_data_cleaned.csv")
model = joblib.load(MODELS_PATH)
feature_names = joblib.load(FEATURES_PATH)

router = APIRouter(prefix="/api/taxi/v1")
app  = FastAPI()

class TaxiInput(BaseModel):
    