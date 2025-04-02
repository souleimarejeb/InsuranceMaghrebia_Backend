from fastapi import FastAPI, HTTPException
from app.models.schema import SignatureRequest
from app.services.signature_service import save_base64
from app.core.config import config
from app.services.ai_clip_service import get_image_embedding
from langchain.embeddings import OpenAIEmbeddings   
import io
from PIL import Image
import numpy as np


app = FastAPI()

SIMILARITY_THRESHOLD = 0.85 
async def upload_signature(signature : SignatureRequest):
    try:
        image_data = save_base64(signature.base64_data)
        image = Image.open(io.BytesIO(image_data))

        # signature_embedding = process_signature(image)

        # search_results = search_signature_in_pinecone(signature_embedding)

        # if search_results:
        #     return {"message": "Signature match found", "status": "success", "match": search_results}

        # store_signature_in_pinecone(signature_embedding, signature.cin)

        return {"message": "Signature added to Pinecone", "status": "added"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# def process_signature(image: Image.Image):
   
#     # signature_features = get_image_embedding(image) 
     
#     model = OpenAIEmbeddings()
#     signature_embedding = model.embed_image(image)
#     return signature_embedding

# def search_signature_in_pinecone(embedding):
#     query_response = config.index.query(queries=[embedding], top_k=1)
#     if query_response["matches"]:
#         return query_response["matches"]
#     return None


# def store_signature_in_pinecone(embedding, signature_id):
#    config.index.upsert(vectors=[(signature_id, embedding)])
#    config.llama_index.add_document(signature_id, embedding)



# def signature(signature : SignatureRequest):
#     try:
#         index = config.index

#         embedding_model = config.embedding_model

#         image=save_base64(signature.base64_data)
#         image_embedding = embedding_model.get_query_embedding(image) 

#         search_results = index.query(
#                 vector=image_embedding,
#                 namespace="signatures",
#                 top_k=1,  
#                 include_values=True,
#                 include_metadata=True
#             )
#         if "matches" in search_results and search_results["matches"]:  
#             best_match = search_results["matches"][0]
#             similarity_score = best_match["score"]

#             if similarity_score >= SIMILARITY_THRESHOLD:
#                 return {
#                     "message": "✅ Signature match successful! Payment can proceed.",
#                     "status": "success",
#                     "score": similarity_score
#                     }
#             else:
#                 return {
#                     "message": "❌ Signature does not match! Payment refused.",
#                     "status": "failed",
#                     "score": similarity_score
#                 }
        
#         signature_id = str(signature.cin)

#         vector = {
#                 "id": signature_id,
#                 "values": image_embedding,
#                 "metadata": {
#                     "full_name": signature.user_id
#                 }
#                 }

#         index.upsert(vectors=[vector], namespace="signatures")

#         return {"message": "🆕 New signature stored successfully!", "signature_id": signature_id}
#     except Exception as e:
#         raise RuntimeError(f"Error inserting signature embedding: {str(e)}")       
    


