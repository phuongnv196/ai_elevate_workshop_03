import chromadb
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY_EMBEDDING"),
    api_version="22024-07-01-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",  
        input=[text]
    )
    return response.data[0].embedding

def build_index(chunks):
    collection_name="default_collection"
    client = chromadb.Client()
    if collection_name in [c.name for c in client.list_collections()]:
        client.delete_collection(collection_name)
    collection = client.create_collection(collection_name)
    vectors = [embed_text(c) for c in chunks]
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        embeddings=vectors,
        documents=chunks,
        ids=ids
    )
    return collection

def search(query, collection, k=5):
    q_vec = embed_text(query)
    results = collection.query(
        query_embeddings=[q_vec],
        n_results=k
    )
    return results["documents"][0] if "documents" in results else []
