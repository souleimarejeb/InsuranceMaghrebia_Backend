from fastapi import FastAPI  
from app.api.routes.signatureRoute import router as signature_router

app= FastAPI()

@app.get("/")
def read_root():
    return {"message ": "Welcome to Signature API !"}   

app.include_router(signature_router, prefix="/signature", tags=["Signature"])