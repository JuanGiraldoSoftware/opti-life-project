from fastapi import FastAPI

app = FastAPI(title="OptiLife API", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to OptiLife!"}
