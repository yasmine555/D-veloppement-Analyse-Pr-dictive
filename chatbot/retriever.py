# chatbot/retriever.py
import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

INDEX_PATH = "chat_index.faiss"
DOCS_PATH = "chat_docs.pkl"
MODEL_NAME = "all-MiniLM-L6-v2"

def _l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True) + 1e-12
    return x / norms

class Retriever:
    def __init__(self, index_path: str = INDEX_PATH, docs_path: str = DOCS_PATH, model_name: str = MODEL_NAME):
        if not os.path.exists(index_path) or not os.path.exists(docs_path):
            raise FileNotFoundError(
                f"[Retriever] Index ou docs manquants.\n"
                f"  - attendu: {index_path}\n"
                f"  - attendu: {docs_path}\n"
                f"👉 Lance d'abord:  python chatbot/index_docs.py --source docs"
            )
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)
        with open(docs_path, "rb") as f:
            data = pickle.load(f)
        self.texts = data["texts"]
        self.metadatas = data["metadatas"]

    def query(self, question: str, k: int = 5):
        q_emb = self.model.encode([question], convert_to_numpy=True)
        q_emb = _l2_normalize(q_emb.astype("float32"))  # pour cosine
        k = min(k, len(self.texts))
        if k <= 0:
            return []
        D, I = self.index.search(q_emb, k)
        results = []
        for rank, idx in enumerate(I[0]):
            if idx < 0:
                continue
            results.append({
                "text": self.texts[idx],
                "meta": self.metadatas[idx],
                "score": float(D[0][rank])  # similarité (IP) si index construit en IP
            })
        return results
