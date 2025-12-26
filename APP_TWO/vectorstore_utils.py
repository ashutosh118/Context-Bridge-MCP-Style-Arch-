import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle

MODEL_NAME = "all-MiniLM-L6-v2"  # Small, fast, local embedding model
INDEX_FILE = "faiss_index.bin"
DOCS_FILE = "faiss_docs.pkl"

class VectorStore:
    def __init__(self, dim=384):
        # Initializes the vector store, acting as an agent for managing embeddings and FAISS index.
        self.model = SentenceTransformer(MODEL_NAME)
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.docs = []
        if os.path.exists(INDEX_FILE) and os.path.exists(DOCS_FILE):
            self.load()

    def add_docs(self, texts):
        # Acts as an agent to index documents into the FAISS vector store.
        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.docs.extend(texts)
        self.save()
    
    def search(self, query, top_k=3):
        # Acts as an agent to retrieve relevant documents based on a query.
        if not self.docs or self.index.ntotal == 0:  # Check if docs or index is empty
            return []  # Return an empty list if no data is available
        embedding = self.model.encode([query])
        D, I = self.index.search(np.array(embedding, dtype=np.float32), top_k)
        results = []
        for i in I[0]:
            if i < len(self.docs):
                doc = self.docs[i]
                if isinstance(doc, dict):
                    # Already has 'text' and 'filename'
                    results.append(doc)
                else:
                    # Backward compatibility: wrap string as dict
                    results.append({"text": doc, "filename": "unknown"})
        return results

    def save(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(DOCS_FILE, "wb") as f:
            pickle.dump(self.docs, f)

    def load(self):
        self.index = faiss.read_index(INDEX_FILE)
        with open(DOCS_FILE, "rb") as f:
            self.docs = pickle.load(f)

    def clear(self):
        # Acts as an agent to clear the FAISS index and associated documents.
        self.index = faiss.IndexFlatL2(self.dim)  # Reinitialize the index
        self.docs = []  # Clear the document list
        if os.path.exists(INDEX_FILE):
            os.remove(INDEX_FILE)  # Remove the index file
        if os.path.exists(DOCS_FILE):
            os.remove(DOCS_FILE)  # Remove the documents file
