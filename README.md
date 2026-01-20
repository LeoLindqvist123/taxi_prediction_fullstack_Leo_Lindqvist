# Taxi Price Prediction

Fullstack ML application for predicting taxi prices.

## Technologies

ML: scikit-learn, pandas  
Backend: FastAPI  
Frontend: Streamlit  
Package Manager: uv

## Installation
```bash
git clone https://github.com/LeoLindqvist123/taxi-prediction-fullstack-Leo_Lindqvist.git
cd taxi-prediction-fullstack-Leo_Lindqvist

uv venv
uv sync
uv pip install fastapi uvicorn streamlit pandas scikit-learn joblib requests
```

## Usage

Terminal 1:
```bash
python -m uvicorn src.taxipred.backend.api:app --reload
```

Terminal 2:
```bash
cd frontend
streamlit run app.py
```

## API Endpoints

GET /api/taxi/v1 - Returns all taxi data  
POST /api/taxi/v1/predict - Predicts taxi price

## Screenshots

![Streamlit Application](images/streamlit_home.png)

![Prediction Result](images/streamlit_prediction.png)

## Model Performance

MAE: 5.6 kr  
R² Score: 0.906

## Author

Leo Lindqvist    
January 2026