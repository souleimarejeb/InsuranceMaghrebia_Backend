import base64
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

def save_base64(base64_str : str ):

    try:
        image_data = base64.b64decode(base64_str.split(",")[-1])  
        return image_data 
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 image data: {str(e)}")
