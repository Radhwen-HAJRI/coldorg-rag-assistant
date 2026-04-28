import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = """Tu es un assistant technique expert pour les techniciens de maintenance CVC.
Base-toi UNIQUEMENT sur les documents fournis. Structure ta réponse avec :
Causes possibles, Procédure de diagnostic, Solution recommandée, Pièces à prévoir."""

def build_context(retrieved_docs, max_chars=6000):
    lines = ["=== DOCUMENTS PERTINENTS ===\n"]
    total = 0
    for i, doc in enumerate(retrieved_docs, 1):
        meta = doc["metadata"]
        block = f"[Source {i} | {meta.get('source','?')} | score: {doc['score']:.2f} | marque: {meta.get('marque','?')}]\n{doc['text']}\n"
        if total + len(block) > max_chars:
            break
        lines.append(block)
        total += len(block)
    return "\n".join(lines)

def generate_response(question, retrieved_docs, model="llama-3.3-70b-versatile", debug=False):
    context = build_context(retrieved_docs)
    if debug:
        return {"answer": "[Mode debug]\n\n" + context, "context": context, "retrieved_docs": retrieved_docs, "model": "debug"}

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{context}\n\n=== QUESTION ===\n{question}"}
        ],
        max_tokens=1024,
    )
    return {
        "answer": response.choices[0].message.content,
        "context": context,
        "retrieved_docs": retrieved_docs,
        "model": model,
    }