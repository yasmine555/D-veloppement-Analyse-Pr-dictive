# chatbot/chat_api.py
from flask import Flask, request, jsonify
from retriever import Retriever
from qa_chain import answer_question
from model_gateway import predict_via_gateway, available_models

app = Flask(__name__)
retriever = None

@app.before_first_request
def _load_retriever():
    global retriever
    try:
        retriever = Retriever()
    except Exception as e:
        # on laisse l'API démarrer, mais on prévient côté /health
        print("[WARN] Retriever not ready:", e)
        retriever = None

@app.route("/health", methods=["GET"])
def health():
    status = {"status": "ok", "retriever_ready": retriever is not None, "models": available_models()}
    return jsonify(status), 200

@app.route("/chat", methods=["POST"])
def chat():
    """
    JSON attendu:
    {
      "question": "texte libre",
      "intent": "sales|churn|...",           (optionnel)
      "data": { ... features pour la prédiction ... }  (optionnel)
    }
    """
    data = request.get_json(force=True, silent=True) or {}
    q = (data.get("question") or "").strip()
    intent = (data.get("intent") or "").strip()
    payload = data.get("data") or {}

    if not q and not intent:
        return jsonify({"error": "missing 'question' or 'intent'"}), 400

    # 1) Si un intent explicite est fourni -> tentative de prédiction
    if intent:
        res = predict_via_gateway(intent, payload)
        if "error" in res:
            return jsonify({"answer": res["error"], "need_data": True}), 200
        return jsonify({"answer": f"Résultat {intent}: {res['prediction']}", "intent": intent}), 200

    # 2) Sinon, simple RAG Q&A
    if retriever is None:
        return jsonify({"answer": "La base documentaire n'est pas prête. Lance d'abord l'indexation."}), 200

    contexts = retriever.query(q, k=5)
    qa = answer_question(q, contexts)
    sources = [c.get("meta", {}).get("source", "") for c in contexts]
    return jsonify({"answer": qa["answer"], "score": qa.get("score", 0.0), "sources": sources}), 200

if __name__ == "__main__":
    # lancement local
    app.run(host="0.0.0.0", port=8001, debug=True)
