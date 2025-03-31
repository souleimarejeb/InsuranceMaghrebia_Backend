from pydantic import BaseModel

class SignatureRequest(BaseModel):
    base64_data: str  
    user_id: str    
    cin: str  
