import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
class Config:
    pc = Pinecone(api_key=os.getenv("SECRET_KEY", "SECRET_KEY"))
    index_name = "signatureTest"
    pc.create_index(
    name=index_name,
    dimension=1024, 
    metric="cosine", 
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)
   

    



config = Config()
