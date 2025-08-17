# chatbot/qa_chain.py
import os
from transformers import pipeline

USE_LOCAL = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"
QA_MODEL = os.getenv("QA_MODEL", "distilbert-base-cased-distilled-squad")
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "3500"))

if USE_LOCAL:
    qa_pipe = pipeline("question-answering", model=QA_MODEL)
else:
    qa_pipe = None  # à remplacer si tu branches un LLM distant

def _trim_context(chunks, max_chars=MAX_CONTEXT_CHARS):
    out, total = [], 0
    for c in chunks:
        t = c["text"]
        if total + len(t) + 2 > max_chars:
            break
        out.append(t)
        total += len(t) + 2
    return "\n\n".join(out)

def answer_question(question, contexts):
    combined_context = _trim_context(contexts, MAX_CONTEXT_CHARS)
    if not combined_context.strip():
        return {"answer": "Je n'ai pas trouvé d'information pertinente dans la base.", "score": 0.0}

    if USE_LOCAL:
        res = qa_pipe(question=question, context=combined_context)
        if isinstance(res, list) and res:
            res = res[0]
        return {"answer": res.get("answer", ""), "score": float(res.get("score", 0.0))}
    else:
        raise NotImplementedError("Remote LLM non configuré")
