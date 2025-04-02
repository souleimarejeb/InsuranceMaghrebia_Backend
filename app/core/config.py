import os
from dotenv import load_dotenv
from pinecone import (
    Pinecone,
    ServerlessSpec,
    CloudProvider,
    AwsRegion,
    VectorType
)
import llama_index
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore  

load_dotenv()
class Config:
    PINECONE_API_KEY = os.getenv("SECRET_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "signature")
    GEMINI_EMBEDDING_API_KEY = os.getenv("GEMINI_EMBEDDING")  

    embedding_model = GeminiEmbedding(
        model_name="models/embedding-001",  
        api_key=GEMINI_EMBEDDING_API_KEY
    )

    llama_index = llama_index.LlamaIndex()

    pc=Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)

    vector_store = PineconeVectorStore(
        pinecone_index=index,
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT
    )
config = Config()
