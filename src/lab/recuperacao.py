"""Busca lexical sobre textos próprios. Não gera respostas com um LLM."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def buscar(query, documents, k=3):
    if not isinstance(query, str) or not 1 <= len(query.strip()) <= 500 or type(k) is not int or not 1 <= k <= 5:
        raise ValueError("Pergunta deve ter até 500 caracteres; k entre 1 e 5.")
    if not isinstance(documents, list) or not 1 <= len(documents) <= 200:
        raise ValueError("Use entre 1 e 200 documentos.")
    if not all(isinstance(d, dict) and set(d) == {"id", "title", "text"} and all(isinstance(v, str) and v for v in d.values()) and len(d["text"]) <= 80_000 for d in documents):
        raise ValueError("Documento inválido.")
    if sum(len(d["text"]) for d in documents) > 2_000_000 or len({d["id"] for d in documents}) != len(documents):
        raise ValueError("Corpus muito grande ou IDs duplicados.")
    vectorizer = TfidfVectorizer(strip_accents="unicode", lowercase=True, ngram_range=(1, 2), max_features=12000)
    try:
        matrix = vectorizer.fit_transform([d["text"] for d in documents])
    except ValueError:
        return []
    scores = cosine_similarity(vectorizer.transform([query]), matrix)[0]
    ordered = sorted(range(len(documents)), key=lambda i: (-scores[i], documents[i]["id"]))
    results = []
    tokens = query.lower().split()
    for i in ordered[:k]:
        if scores[i] <= 0:
            continue
        doc = documents[i]
        paragraphs = [p.strip() for p in doc["text"].split("\n\n") if p.strip()]
        passage = max(paragraphs, key=lambda p: sum(t in p.lower() for t in tokens)) if paragraphs else doc["text"]
        results.append({"id": doc["id"], "title": doc["title"], "score": float(scores[i]), "trecho": passage[:900]})
    return results


def _validar_casos(cases, documents):
    if not isinstance(cases, list) or not cases or len(cases) > 100:
        raise ValueError("Conjunto de avaliação inválido.")
    if not all(isinstance(c, dict) and set(c) == {"query", "expected"} and isinstance(c["query"], str) and isinstance(c["expected"], str) and c["expected"] in {d["id"] for d in documents} for c in cases):
        raise ValueError("Caso de avaliação inválido.")


def recall_at_k(cases, documents, k=3):
    _validar_casos(cases, documents)
    rows = []
    for case in cases:
        result = buscar(case["query"], documents, k)
        rows.append({"pergunta": case["query"], "esperado": case["expected"], "acerto": case["expected"] in {r["id"] for r in result}})
    return sum(r["acerto"] for r in rows) / len(rows), rows


def mrr_at_k(cases, documents, k=5):
    """Mean Reciprocal Rank: 1/posição do documento esperado (0 se ficar fora do top-k)."""
    _validar_casos(cases, documents)
    total = 0.0
    for case in cases:
        ids = [r["id"] for r in buscar(case["query"], documents, k)]
        total += 1 / (ids.index(case["expected"]) + 1) if case["expected"] in ids else 0.0
    return total / len(cases)


def taxa_de_abstencao(queries, documents, limiar=0.0):
    """Fração de perguntas fora do escopo em que a busca devolve nada acima do limiar.

    TF-IDF sempre devolve algo se houver uma palavra em comum; sem limiar, ele não se abstém.
    """
    if not isinstance(queries, list) or not queries or len(queries) > 100 or not all(isinstance(q, str) for q in queries):
        raise ValueError("Use de 1 a 100 perguntas de texto.")
    if not isinstance(limiar, (int, float)) or isinstance(limiar, bool) or not 0 <= limiar <= 1:
        raise ValueError("Limiar deve ficar entre 0 e 1.")
    silent = sum(not [r for r in buscar(q, documents, 1) if r["score"] > limiar] for q in queries)
    return silent / len(queries)
