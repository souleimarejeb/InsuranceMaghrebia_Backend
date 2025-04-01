import time
import uuid
from app.core.config import config
from pinecone import Pinecone, ServerlessSpec
from app.models.schema import SignatureRequest
from app.services.ai_clip_service import get_image_embedding
from app.services.signature_service import save_base64
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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
        index = pc.Index(config.PINECONE_INDEX_NAME)
        
        fetch_result=index.fetch(ids=[signture.cin], namespace="signatures")

        if signture.cin not in fetch_result.vectors:
            image=save_base64(signture.base64_data)
            image_embedding= get_image_embedding(image)

            while not pc.describe_index(config.PINECONE_INDEX_NAME).status['ready']:
                time.sleep(1)
       
            vector = {
                "id": signture.cin,  
                "values": image_embedding,
                "metadata": {
                "full_name": signture.user_id,
                }
            }
            index.upsert(
            vectors=[vector],  
            namespace="signatures" 
            )
            return {"message": f"Signature stored successfully for {signture.user_id}", "signature_id": signture.cin}
        
            
        image = save_base64(signture.base64_data)
        new_embedding = get_image_embedding(image)

        stored_embedding = np.array(fetch_result.vectors[signture.cin].values)
        new_embedding = np.array(new_embedding)
    
        similarity_score = cosine_similarity([stored_embedding], [new_embedding])[0][0]

        SIMILARITY_THRESHOLD = 0.85
        if(similarity_score >=SIMILARITY_THRESHOLD):

            return {
                "message": f"Signature match successful ! payment can proceed",
                "status":"success",
                "score":similarity_score}
        else :
            return {
                "message": f"Signature dont match ! payment refused ",
                "status":"failed",
                "score":similarity_score
            }    
    
    except Exception as e:
        raise RuntimeError(f"Error inserting signature embedding: {str(e)}")
