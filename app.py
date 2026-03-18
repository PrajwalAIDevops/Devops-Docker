from fastapi import FastAPI

app = FastAPI()

# 1st API
@app.get("/api1")
def api_one():
    return {"message": "EC2 API 1 response end"}

# 2nd API
@app.get("/api2")
def api_two():
    return {"message": "EC2 API 2 response end"}

# 3rd API
@app.get("/api3")
def api_three():
    return {"message": "EC2 API 3 response end"}

# 4th API
@app.get("/api4")
def api_four():
    return {"message": "EC2 API 4 response end"}

# 5th API
@app.get("/api5")
def api_five():
    return {"message": "EC2 API 5 response end"}