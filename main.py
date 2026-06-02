from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
import json
from models import Patient


app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)
    
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Enrollment API"}


@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your patient records.'}

@app.get("/view")
def view_patients():
    patient_data = load_data()
    return patient_data

# Endpoint with path parameter
@app.get("/patient/{patiend_id}")
def get_patient(patiend_id : str = Path(..., description= "ID of a Patient", examples = ["P001"])):
    patient_data = load_data()
    if patiend_id in patient_data:
        return patient_data[patiend_id]
    # return {'Error':'Patient not found!'}
    raise HTTPException(status_code=404, detail="Patient not found!")

# Enpoint with query parameter
@app.get("/patient_sort")
def view_sorted_patient(sort_by : str = Query(..., decsription= "Sorting patient details based on height or weight or age or bmi", examples = ['Height']),
                        order : str  = Query('asc', description= "Sorting order of asc or desc")):
    
    patient_data = load_data()

    sort_by_list = ['height', 'weight', 'age', 'bmi']
    sort_order = True if order == 'desc' else False

    if sort_by not in sort_by_list:
        raise HTTPException(status_code=400, detail = 'Invalid sort by value selected')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = 'Invalid sorting order selected')
    
    sorted_data = sorted(patient_data.values(), key = lambda x : x.get(sort_by, 0), reverse=sort_order )

    return sorted_data

@app.post("/addPatient")
def create_patient(patient: Patient):

    patient_data = load_data()

    if patient.id in patient_data:
        raise HTTPException(status_code=400, detail= 'Patient already exists')
    
    patient_data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(patient_data)

    return JSONResponse(status_code=201, content='Patient successfully created')
