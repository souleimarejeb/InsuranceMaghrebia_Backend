import base64
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from llama_index.embeddings.openai import OpenAIEmbedding
from io import BytesIO
from PIL import Image  
import io  

embedding_model = OpenAIEmbedding(model="text-embedding-ada-002")

def save_base64(base64_str : str ):

    try:
        image_data = base64.b64decode(base64_str.split(",")[-1]) 
        # image = Image.open(BytesIO(image_data))   
        image = Image.open(io.BytesIO(image_data))    
        return image
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 image data: {str(e)}")

