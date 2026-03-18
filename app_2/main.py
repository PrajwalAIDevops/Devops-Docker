from fastapi import FastAPI

app = FastAPI()

# 6th API - Get Products
@app.get("/products")
def get_products():
    return {"message": "EC2 Fetching all products EC2 -2"}

# 7th API - Get Orders
@app.get("/orders")
def get_orders():
    return {"message": "EC2 Fetching all orders EC2 -2"}

# 8th API - Get Cart
@app.get("/cart")
def get_cart():
    return {"message": "EC2 Fetching user cart EC2 -2"}

# 9th API - Add Product
@app.post("/add-product")
def add_product():
    return {"message": "EC2 Product added successfully EC2 -2"}

# 10th API - Checkout
@app.post("/checkout")
def checkout():
    return {"message": "EC2 Order placed successfully EC2 -2"}