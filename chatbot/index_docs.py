# chatbot/index_docs.py
import os
import glob
import argparse
import pickle
import numpy as np
import faiss
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
EMB_DIM = 384
INDEX_PATH = "chat_index.faiss"
DOCS_PATH = "chat_docs.pkl"

def read_txt_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += max(1, chunk_size - overlap)
    return chunks

def l2_normalize(mat: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(mat, axis=1, keepdims=True) + 1e-12
    return mat / norms

def main(source_folder="docs"):
    model = SentenceTransformer(MODEL_NAME)
    texts, metadatas = [], []

    exts = ("*.md", "*.txt", "*.csv", "*.py", "*.ipynb")
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(source_folder, "**", ext), recursive=True))
    if not files:
        print(f"Aucun fichier trouvé dans {source_folder}")
        return

    for path in tqdm(files, desc="Indexation"):
        try:
            if path.endswith(".ipynb"):
                import nbformat
                nb = nbformat.read(path, as_version=4)
                cells = [c.get("source","") for c in nb.cells if c.get("cell_type") in ("markdown","code")]
                raw = "\n".join(cells)
            elif path.endswith(".csv"):
                import pandas as pd
                raw = pd.read_csv(path, nrows=1000).to_string()
            else:
                raw = read_txt_file(path)

            for c in chunk_text(raw, chunk_size=500, overlap=50):
                texts.append(c)
                metadatas.append({"source": path})
        except Exception as e:
            print("skip", path, e)

    if not texts:
        print("Aucun chunk généré.")
        return

    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True).astype("float32")
    embeddings = l2_normalize(embeddings)  # pour cosine

    # Index cosine ≈ Inner Product sur vecteurs normalisés
    index = faiss.IndexFlatIP(EMB_DIM)
    index.add(embeddings)

    with open(DOCS_PATH, "wb") as f:
        pickle.dump({"texts": texts, "metadatas": metadatas}, f)
    faiss.write_index(index, INDEX_PATH)
    print(f"Index saved: {INDEX_PATH}, {DOCS_PATH}")
    print(f"Documents: {len(texts)} chunks, dim={EMB_DIM}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="docs", help="Dossier à indexer")
    args = parser.parse_args()
    main(args.source)
