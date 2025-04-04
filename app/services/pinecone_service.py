import time
import uuid
from app.core.config import config
from pinecone import Pinecone, ServerlessSpec
from app.models.schema import SignatureRequest
from app.services.ai_clip_service import get_image_embedding
from app.services.signature_service import save_base64


def initialize_pinecone():

    pineconeInst = Pinecone(api_key=config.PINECONE_API_KEY)

    existing_indexes = pineconeInst.list_indexes().names()
    print("Existing Indexes:", existing_indexes)

    if config.PINECONE_INDEX_NAME not in pineconeInst.list_indexes().names():
        pineconeInst.create_index(
            name=config.PINECONE_INDEX_NAME,
            dimension=512, 
            metric='cosine',  
            spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
    ) 
        )
    index = pineconeInst.Index(config.PINECONE_INDEX_NAME)
    print("Index Object:", index)
    return index


def insert_signature_embedding(signture : SignatureRequest):
   
    try:
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        
        image=save_base64(signture.base64_data)
        image_embedding= get_image_embedding(image)

        while not pc.describe_index(config.PINECONE_INDEX_NAME).status['ready']:
            time.sleep(1)
        
        index = pc.Index(config.PINECONE_INDEX_NAME)
        signature_id =str(uuid.uuid4())
        vector = {
            "id": signature_id,  
            "values": image_embedding,
            "metadata": {
                "full_name": signture.user_id,
                "cin": signture.cin
            }
        }
        
        index.upsert(
            vectors=[vector],  
            namespace="signatures"
        )

        return {"message": "Signature stored successfully", "signature_id": signature_id}
    
    except Exception as e:
        raise RuntimeError(f"Error inserting signature embedding: {str(e)}")
