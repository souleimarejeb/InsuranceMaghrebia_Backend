from fastapi import APIRouter, HTTPException
from app.models.schema import SignatureRequest
from app.services.pinecone_service import insert_signature_embedding

router = APIRouter()

@router.post("/storeSign")
async def store_signature(signature: SignatureRequest):
    try:    
        return {"message": "Signature stored successfully!", "user_id": signature.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/add")
async def add(signature: SignatureRequest):
    try:  
        response= insert_signature_embedding(signature)  
        return {"message": response["message"], "signature_id": signature.cin}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
