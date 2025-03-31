import time
import pinecone
from app.core.config import config
from pinecone import Pinecone, ServerlessSpec


def initialize_pinecone():

    pineconeInst = Pinecone(api_key=config.PINECONE_API_KEY)

    existing_indexes = pineconeInst.list_indexes().names()
    print("Existing Indexes:", existing_indexes)

    if config.PINECONE_INDEX_NAME not in pineconeInst.list_indexes().names():
        pineconeInst.create_index(
            name=config.PINECONE_INDEX_NAME,
            dimension=1024, 
            metric='cosine',  
            spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
    ) 
        )
    index = pineconeInst.Index(config.PINECONE_INDEX_NAME)
    print("Index Object:", index)
    return index


def insert_pinecone(data, embeddings):

    pc= Pinecone(api_key=config.PINECONE_API_KEY)

    while not pc.describe_index(config.PINECONE_INDEX_NAME).status['ready']:
        time.sleep(1)
            
    index = pc.Index(config.PINECONE_INDEX_NAME)
    vectors = []
    for d, e in zip(data, embeddings):
        vectors.append({
        "id": d['id'],
        "values": e['values'],
        "metadata": {'text': d['text']}
    })
    index.upsert(
            vectors=vectors,
            namespace="ns1"
        )    

    return vectors