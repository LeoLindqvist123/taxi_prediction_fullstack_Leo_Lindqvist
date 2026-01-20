from fastapi import FastAPI, APIRouter
import pandas as pd
import joblib
from pathlib import Path
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).parent.parent

DATA_PATH = Path(__file__).parent / "data"
MODEL_PATH = BASE_DIR / "model_development" / "model.joblib"
FEATURES_PATH = BASE_DIR / "model_development" / "feature_names.joblib"

df = pd.read_csv(DATA_PATH / "taxi_data_cleaned.csv")
model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURES_PATH)

router = APIRouter(prefix="/api/taxi/v1")
app  = FastAPI()

class TaxiInput(BaseModel):
    Trip_Distance_km: float = Field(gt=0, lt=100)
    Time_of_Day: str
    Day_of_Week: str
    Passenger_Count: int = Field(ge=1, le=8)
    Weather: str
    Base_Fare: float = Field(gt=0)
    Per_Km_Rate: float = Field(gt=0)
    Per_Minute_Rate: float = Field(gt=0)
    Trip_Duration_Minutes: float = Field(gt=0)
    traffic_conditions: str

class PredictionOutput(BaseModel):
    predicted_price: float

@router.get("")
def read_data():
    return df.to_dict(orient="records")

@router.post("/predict", response_model=PredictionOutput)
def predict_price(payload: TaxiInput):
    
    data_to_predict = pd.DataFrame(payload.model_dump(), index=[0])
    
    data_encoded = pd.get_dummies(data_to_predict, drop_first=True)

    for col in feature_names:
        if col not in data_encoded.columns:
            data_encoded[col] = 0

    data_encoded = data_encoded[feature_names]

    prediction = model.predict(data_encoded)
    
    return {"predicted_price": float(prediction[0])}

app.include_router(router=router)