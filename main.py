from fastapi import FastAPI, Path, Query, HTTPException
import json


app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

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
def view_patients(patiend_id : str = Path(..., description= "ID of a Patient", example= "P001")):
    patient_data = load_data()
    if patiend_id in patient_data:
        return patient_data[patiend_id]
    # return {'Error':'Patient not found!'}
    raise HTTPException(status_code=404, detail="Patient not found!")

# Enpoint with query parameter
@app.get("/patient_sort")
def view_sorted_patient(sort_by : str = Query(..., decsription= "Sorting patient details based on height or weight or age or bmi", example = 'Height'),
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