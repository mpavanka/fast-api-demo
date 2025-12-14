from fastapi import FastAPI
from model import products

app = FastAPI()

model = [ 

    products(id=2, name="Headphones", description="Noise-cancelling headphones", price=200.00, quality=7),
    products(id=3, name="Monitor", description="4K UHD Monitor", price=400.00, quality=8),
    products(id=4, name="Smartphone", description="Latest model smartphone", price=800.00, quality=8),
    products(id=5, name="Keyboard", description="Mechanical keyboard", price=100.00, quality=9)
    
]   

@app.get("/product")
def greeting():
    return model

@app.get("/product/{product_id}")
def get_product_by_id(product_id: int):
    for product in model:
        if product.id == product_id:
            return product
    return {"Error": "Product not found"}

@app.post("/product")
def addProduct(new_product: products):
    model.append(new_product)
    return "Product added successfully"

@app.delete("/delete/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(model):
        if product.id == product_id:
            model.pop(index)
            return "Product deleted successfully"
    return {"Error": "Product not found"}

@app.put("/update/{product_id}")
def update(product_id: int, updated_product: products):
    for index, product in enumerate(model):
        if product.id == product_id:
            model[index] = updated_product
            return "Product quality updated successfully"
    return {"Error": "Product not found"}