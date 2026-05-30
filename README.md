# FastAPI
This repository serves as a collection of FastAPI tutorials, examples, and projects created to learn and demonstrate FastAPI concepts.

# Fetaures
      GET /: Welcome endpoint
      GET /products/: Get all products
      GET /products/{product_id}: Get a specific product by ID
      POST /products/: Create a new product
      PUT /products/: Update an existing product
      PATCH /products/: Partially update an existing product
      DELETE /products/: Deletes an existing product

# Setup 
      1. Create and activate virtual environment:
            python -m venv myenv
            myenv\Scripts\activate.ps1  # Windows PowerShell
   
      2. Install dependencies:
            pip install fastapi uvicorn   
   
      3. Run the application:
            uvicorn main:app --reload
   
      4. Access the API:
            API: http://localhost:8000
            Interactive SwaggerUI docs: http://localhost:8000/docs
            ReDoc: http://localhost:8000/redoc

# Models

## Product
    id: integer
    name: string
    description: string
    price: float
    quantity: integer

# Built With
    FastAPI - Modern, fast web framework for building APIs
    Pydantic - Data validation using Python type hints
    SQLAlchemy -  Python SQL toolkit and Object Relational Mapper
    Uvicorn - ASGI server implementation
