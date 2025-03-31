import base64
from io import BytesIO
from PIL import Image
from fastapi import APIRouter, HTTPException
from app.models.schema import SignatureData


def save_base64(base64_str : str , file_path:str ):
    """
    Converts a base64 string to an image and saves it.
    """

    try:
        image_data = base64.b64decode(base64_str.split(",")[-1])  
        image = Image.open(BytesIO(image_data))
        image.save(file_path, format="PNG")  
        return file_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 image data: {str(e)}")
