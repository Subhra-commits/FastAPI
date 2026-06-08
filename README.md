# FastAPI
This repository serves as a collection of FastAPI tutorials, examples, and projects created to learn and demonstrate FastAPI concepts.

# Fetaures
      GET /: Welcome endpoint
      GET /about/: About the API
      GET /view/: View all patients
      GET /patient/{patiend_id}: Get a specific patient by ID
      GET /patient_sort: Get patient details in sorting order
      POST /addPatient/: Create a new patient
      PUT /edit/{patient_id}/: Update an existing patient
      PATCH /products/: Partially update an existing product
      DELETE /delete/{patient_id}/: Deletes an existing patient

# Setup 
      1. Create and activate virtual environment:
            python -m venv myenv
            myenv\Scripts\activate.ps1  # Windows PowerShell
   
      2. Install dependencies:
            pip install fastapi uvicorn 
            or pip install -r requirements.txt
   
      3. Run the application:
            uvicorn main:app --reload
   
      4. Access the API:
            API: http://localhost:8000
            Interactive SwaggerUI docs: http://localhost:8000/docs
            ReDoc: http://localhost:8000/redoc

# Models

## Product
    id: str
    name: str
    city: str
    age: int
    gender: Literal
    height: float
    weight: float
    bmi: computed_value
    verdict: computed_value

# Built With
    FastAPI - Modern, fast web framework for building APIs
    Pydantic - Data validation using Python type hints
    SQLAlchemy -  Python SQL toolkit and Object Relational Mapper
    Uvicorn - ASGI server implementation
