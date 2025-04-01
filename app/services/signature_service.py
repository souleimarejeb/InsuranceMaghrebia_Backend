import base64
from fastapi import APIRouter, HTTPException



def save_base64(base64_str : str , file_path:str ):
    """
    Converts a base64 string to an image and saves it.
    """

    try:
        image_data = base64.b64decode(base64_str.split(",")[-1])  
        return image_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 image data: {str(e)}")
