from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.request_model import UserInput
from schema.response_model import PredictedResponse
from model.predict import model, MODEL_VERSION, predict_output

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(status_code= 200, content={'message' : 'Welcome to the Insurance Premium Prediction API'})

@app.get("/health")
def health_check():
    return JSONResponse(status_code= 200, content={'status': 'OK', 'model_version': MODEL_VERSION})

@app.post("/predict", response_model= PredictedResponse)
def predict_premium(userData : UserInput):
    user_input = {
        'age': userData.age,
        'weight': userData.weight,
        'height': userData.height,
        'smoker': userData.smoker,
        'city': userData.city,
        'income_lpa': userData.income_lpa,
        'occupation': userData.occupation
    }

    try:
        premium_prediction = predict_output(user_input)
        return JSONResponse(status_code= 200, content={'Response' : premium_prediction})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={'error': str(e)})

    