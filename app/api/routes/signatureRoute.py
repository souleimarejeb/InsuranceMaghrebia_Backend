from fastapi import APIRouter, HTTPException
from app.models.schema import SignatureRequest
from app.services.pinecone_service import initialize_pinecone,insert_pinecone
from pinecone import Pinecone
from app.core.config import config
router = APIRouter()

@router.post("/storeSign")
async def store_signature(signature: SignatureRequest):
    try:    
        return {"message": "Signature stored successfully!", "user_id": signature.user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/testpincone")
async def testPinecone():
    try:
       
        pinecone_index = initialize_pinecone()
        
        data = [
            {"id": "vec77", "text": "Apple is a popular fruit known for its sweetness and crisp texture."},
            {"id": "vec55", "text": "The tech company Apple is known for its innovative products like the iPhone."},
            {"id": "vec54", "text": "Many people enjoy eating apples as a healthy snack."},
            {"id": "vec44", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces."},
            {"id": "vec57", "text": "An apple a day keeps the doctor away, as the saying goes."},
            {"id": "vec6", "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership."}
        ]

       
        pc= Pinecone(api_key=config.PINECONE_API_KEY)
        embeddings = pc.inference.embed(
            model="multilingual-e5-large", 
            inputs=[d['text'] for d in data],
            parameters={"input_type": "passage", "truncate": "END"}
        )
       
        vectors=insert_pinecone(data, embeddings)

        return {
            "message": "Vectors stored successfully",
            "stored_vectors": vectors
        }
    

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))