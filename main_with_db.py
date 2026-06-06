from fastapi import FastAPI, Path, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
import json
from models import Patient, PatientUpdate
from db_config import session, db_engine
import db_models
from sqlalchemy.orm import Session


app = FastAPI()

db_models.Base.metadata.create_all(bind = db_engine)

# Get db connection that can be used in other methods
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)
    
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

def init_db():
    db = session()
    patient_data = load_data()

    # count = db.query(db_models.Patients).count()

    for patient_id, patient_info in patient_data.items():
        existing_patient = db.query(db_models.Patients).filter(db_models.Patients.id == patient_id).first()
        if not existing_patient:
            new_patient = db_models.Patients(
                id = patient_id,
                name = patient_info.get('name'),
                city = patient_info.get('city'),
                age = patient_info.get('age'),
                gender = patient_info.get('gender'),
                height = patient_info.get('height'),
                weight = patient_info.get('weight'),
                bmi = patient_info.get('bmi'),
                verdict = patient_info.get('verdict')
            )           
            db.add(new_patient)
    db.commit()

init_db()


@app.get("/")
def hello():
    return {"message": "Patient Enrollment API"}


@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your patient records.'}

@app.get("/view")
def view_patients(db:Session = Depends(get_db)):
    patient_data = db.query(db_models.Patients).all()
    if patient_data:
        return patient_data
    raise HTTPException(status_code=404, detail="No Patient found!")

# Endpoint with path parameter
@app.get("/patient/{patient_id}")
def get_patient(db:Session = Depends(get_db), patient_id : str = Path(..., description= "ID of a Patient", examples = ["P001"])):
    patient_id = patient_id.upper()
    patient_data = db.query(db_models.Patients).filter(db_models.Patients.id == patient_id).first()
    if patient_data:
        return patient_data

    raise HTTPException(status_code=404, detail="Patient not found!")

# Enpoint with query parameter
@app.get("/patient_sort")
def view_sorted_patient(db:Session = Depends(get_db), sort_by : str = Query(..., description= "Sorting patient details based on height or weight or age or bmi", examples = ['Height']),
                        order : str  = Query('asc', description= "Sorting order of asc or desc")):

    sort_by_list = ['height', 'weight', 'age', 'bmi']

    if sort_by not in sort_by_list:
        raise HTTPException(status_code=400, detail = 'Invalid sort by value selected')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code = 400, detail = 'Invalid sorting order selected')    
    
    sort_col = getattr(db_models.Patients, sort_by)
    sort_order = sort_col.desc() if order == "desc" else sort_col.asc()
    sorted_patient_data = db.query(db_models.Patients).order_by(sort_order).all()

    return sorted_patient_data

@app.post("/addPatient")
def create_patient(patient: Patient, db:Session = Depends(get_db)):

    is_patient_exists = db.query(db_models.Patients).filter(db_models.Patients.id == patient.id).first()

    if is_patient_exists:
        raise HTTPException(status_code=400, detail= 'Patient already exists')
    
    db.add(db_models.Patients(**patient.model_dump()))
    db.commit()

    return JSONResponse(status_code=201, content='Patient successfully created')

@app.put("/edit/{patient_id}")
def update_patient(new_data: PatientUpdate, patient_id: str = Path(..., description='Patient ID'), db:Session = Depends(get_db)):
   
    patient_id = patient_id.upper()
    patient_data = db.query(db_models.Patients).filter(db_models.Patients.id == patient_id).first()

    if not patient_data:
        raise HTTPException(status_code = 404, detail = 'Patient not found!')

    updated_patient_info = new_data.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        setattr(patient_data, key, value)

    patient_obj = Patient(
        id=patient_data.id,
        name=patient_data.name,
        city=patient_data.city,
        age=patient_data.age,
        gender=patient_data.gender,
        height=patient_data.height,
        weight=patient_data.weight,
    )

    patient_data.bmi = patient_obj.bmi
    patient_data.verdict = patient_obj.verdict

    db.commit()
    db.refresh(patient_data)

    return JSONResponse(status_code = 200, content = {'message' : 'Patient details updated successfully'})


@app.delete("/delete/{patient_id}")
def delete_patient(db:Session = Depends(get_db), patient_id: str = Path(..., description='Patient ID')):

    patient_id = patient_id.upper()
    patient_data = db.query(db_models.Patients).filter(db_models.Patients.id == patient_id).first()

    if not patient_data:
        raise HTTPException(status_code = 404, detail = 'Patient not found!')
    
    db.delete(patient_data)
    db.commit()

    return JSONResponse(status_code = 200, content = {'message' : 'Patient details deleted successfully'})