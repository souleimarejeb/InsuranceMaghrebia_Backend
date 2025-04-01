from fastapi import APIRouter, HTTPException
from app.models.schema import SignatureRequest,SignatureData
from app.services.pinecone_service import insert_signature_embedding


router = APIRouter()

@router.post("/storeSign")
async def store_signature(signature: SignatureRequest):
    try:    
        return {"message": "Signature stored successfully!", "user_id": signature.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/store")
async def insert(data: SignatureData):
    try:     
        saved_path = insert_signature_embedding(data) 
        return {"message": "Signature stored successfully!", "data": saved_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
