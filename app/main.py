from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from model import products
import productModel
from database import engine, LocalSession
from sqlalchemy.orm import Session

app = FastAPI()

productModel.Base.metadata.create_all(bind=engine)

model = [ 

    products(id=2, name="Headphones", description="Noise-cancelling headphones", price=200.00, quantity=7),
    products(id=3, name="Monitor", description="4K UHD Monitor", price=400.00, quantity=8),
    products(id=4, name="Smartphone", description="Latest model smartphone", price=800.00, quantity=8),
    products(id=5, name="Keyboard", description="Mechanical keyboard", price=100.00, quantity=9)
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

# def initialize_database():
#     db = LocalSession()
#     try:
#         for product in model:
#             db.add(productModel.ProductModel(**product.model_dump()))
#         db.commit()
#     finally:
#         db.close()

# initialize_database()

@app.get("/products")
def greeting(db: Session = Depends(get_db)):
    products = db.query(productModel.ProductModel).all()
    return products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(productModel.ProductModel).filter(productModel.ProductModel.id == product_id).first()
    if product:
        return product
    return {"Error": "Product not found"}

@app.post("/products")
def addProduct(new_product: products, db: Session = Depends(get_db)):
    db.add(productModel.ProductModel(**new_product.model_dump()))
    db.commit()
    return "Product added successfully"

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(productModel.ProductModel).filter(productModel.ProductModel.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return "Product deleted successfully"
    return {"Error": "Product not found"}

@app.put("/products/{product_id}")
def update(product_id: int, updated_product: products, db: Session = Depends(get_db)):
    product = db.query(productModel.ProductModel).filter(productModel.ProductModel.id == product_id).first()
    if product:
        db.query(productModel.ProductModel).filter(productModel.ProductModel.id == product_id).update(updated_product.model_dump())
        db.commit()
        return "Product updated successfully"
    return {"Error": "Product not found"}