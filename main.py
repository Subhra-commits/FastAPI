from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Products
from db_config import session, db_engine
import db_models
from sqlalchemy.orm import Session

app = FastAPI()

# Middleware added for CORS handling to allow requests from frontend running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

db_models.Base.metadata.create_all(bind = db_engine)

# Simple get method
@app.get("/")
def greet():
    return "Welcome to FastAPI Tutorial!"


products = [
    Products(id = 1, name = "Phone", description = "Android", price = 99.5, quantity = "10"),
    Products(id = "2", name = 'Laptop', description = "Macbook", price = 800, quantity = 5),
    Products(id = 3, name = "Tab" , description = "Apple", price = 350, quantity = 9)
]

# Get db connection that can be used in other methods
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

# Initializing data into db if empty
def init_db():
    db = session()
    count = db.query(db_models.Products).count()

    if count == 0:
        for prod in products:
            db.add(db_models.Products(**prod.model_dump()))
        db.commit()

init_db()

# Get all products
@app.get("/products")
def get_all_products(db:Session = Depends(get_db)): # Dependency Injection
    db_products = db.query(db_models.Products).all()
    if db_products:
        return db_products
    return "Product list is empty!"

# Get product by id
@app.get("/products/{id}")
def get_product_by_id(id: int, db:Session = Depends(get_db)): # Dependency Injection
    db_product = db.query(db_models.Products).filter(db_models.Products.id == id).first()
    if db_product:
        return db_product
        
    return "Product Not Found!"

# Get product by name
@app.get("/products/name/{name}")
def get_product_by_name(name: str, db:Session = Depends(get_db)): # Dependency Injection
    db_product = db.query(db_models.Products).filter(db_models.Products.name == name).first()
    if db_product:
        return db_product
        
    return "Product Not Found!"

# Add a new product
@app.post("/products")
def add_product(prod: Products, db:Session = Depends(get_db)): # Dependency Injection
    db.add(db_models.Products(**prod.model_dump()))
    db.commit()
    return prod

# Update a product
@app.put("/products/{id}")
def update_product(id: int, prod: Products, db:Session = Depends(get_db)): # Dependency Injection
    db_product = db.query(db_models.Products).filter(db_models.Products.id == id).first()
    if db_product:
        db_product.name = prod.name
        db_product.description = prod.description
        db_product.price = prod.price
        db_product.quantity = prod.quantity
        db.commit()
        return "Product Updated Succesfully"
        
    return "Product not found!"

# Update a product partially
@app.patch("/products/{id}")
def update_product_part(id: int, name: str, db:Session = Depends(get_db)): # Dependency Injection
    db_product = db.query(db_models.Products).filter(db_models.Products.id == id).first()
    if db_product:
        db_product.name = name
        db.commit()
        return "Product Succesfully Patched"
        
    return "Product not found!"

# Delete a product
@app.delete("/products/{id}")
def delete_product(id: int, db:Session = Depends(get_db)): # Dependency Injection
    db_product = db.query(db_models.Products).filter(db_models.Products.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Succesfully"
        
    return "Product not found!"