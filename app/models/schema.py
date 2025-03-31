from pydantic import BaseModel

class SignatureRequest(BaseModel):
    base64_data: str  
    user_id: str    
    cin: str  

class SignatureData(BaseModel):
    signature_base64:str