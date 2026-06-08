# FastAPI
This repository serves as a collection of FastAPI tutorials, examples, and projects created to learn and demonstrate FastAPI concepts.

# Fetaures
      GET /: Welcome endpoint
      GET /health: Health checkup
      POST /predict/: Predict the premium amount

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
      #Request Model
          age: int
          weight: float
          height: float
          income_lpa: float
          smoker: bool
          city: str
          occupation: Literal

      #Response Model
            predicted_premium: str
            confidence_score: float
            class_probabilities: Dict

# Built With
    FastAPI - Modern, fast web framework for building APIs
    Pydantic - Data validation using Python type hints
    SQLAlchemy -  Python SQL toolkit and Object Relational Mapper
    Uvicorn - ASGI server implementation
