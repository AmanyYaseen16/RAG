import re
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import faiss
from together import Together
import time
# Load data
chunks_df = pd.read_csv("cleaned_chunks.csv")
chunks = chunks_df["chunk"].tolist()
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = np.load("chunk_embeddings.npy")
index = faiss.read_index("chunk_faiss_index.idx")

# Chunk retriever
def retrieve_chunks(query, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=top_k)
    return "\n".join(chunks[i] for i in indices[0])



# Initialize the client
client = Together(api_key="b6d3e1f699ac30c2e615c4951e08558724e409f92ea2f81b83dea25d9d7259a5")

def rag_chat(query, context):
    prompt = f"""Answer the question based on the context below. If the answer is not in the context, say "I don't know."

Context:
{context}

Question:
{query}

Answer:"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500,
        stream=True  # Streaming mode is okay even without printing
    )

    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content

    return full_response.strip()
