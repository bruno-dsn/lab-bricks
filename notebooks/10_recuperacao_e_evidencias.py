# Databricks notebook source

# MAGIC %md
# MAGIC # 10 · Lab Bricks / recuperação lexical verificável
# MAGIC Corpus de notas próprias e busca TF-IDF. Não usa PDFs dos livros, embeddings remotos, API ou geração por LLM. Score é similaridade, não probabilidade de estar correto.

# COMMAND ----------

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


def recall_at_k(cases, documents, k=3):
    if not isinstance(cases, list) or not cases or len(cases) > 100:
        raise ValueError("Conjunto de avaliação inválido.")
    if not all(isinstance(c, dict) and set(c) == {"query", "expected"} and isinstance(c["query"], str) and isinstance(c["expected"], str) and c["expected"] in {d["id"] for d in documents} for c in cases):
        raise ValueError("Caso de avaliação inválido.")
    rows = []
    for case in cases:
        result = buscar(case["query"], documents, k)
        rows.append({"pergunta": case["query"], "esperado": case["expected"], "acerto": case["expected"] in {r["id"] for r in result}})
    return sum(r["acerto"] for r in rows) / len(rows), rows


# COMMAND ----------

notas = [
    {'id': 'delta', 'title': 'Versões e MERGE', 'text': 'MERGE aplica inserções e atualizações por chave. A origem deve ter uma versão candidata por chave. Uma atualização antiga não vence a mais recente. Repetir um lote precisa preservar o conteúdo do destino.'},
    {'id': 'temporal', 'title': 'Features no tempo', 'text': 'Vazamento temporal acontece quando o modelo usa informação do futuro. A média móvel deve usar shift antes de rolling. O scaler aprende somente no treino. Duração real da entrega não está disponível antes da viagem.'},
    {'id': 'acesso', 'title': 'Permissão e namespace', 'text': 'Unity Catalog controla acesso por privilégios. Um schema com hash do usuário evita colisão de nomes, mas não cria autorização. Credenciais e tokens ficam fora do repositório e das saídas de notebooks.'},
    {'id': 'bi', 'title': 'Pedidos e itens', 'text': 'Um pedido pode ter vários itens. Depois do JOIN, COUNT DISTINCT conta pedidos e COUNT estrela conta linhas de itens. Receita considera pedidos concluídos. Margem bruta subtrai custo de mercadoria, não despesas.'},
]
for item in buscar('Como evitar informação do futuro nas features?', notas, 2):
    print(item)
score, detalhes = recall_at_k([
    {'query': 'MERGE versão atualização chave', 'expected': 'delta'},
    {'query': 'vazamento temporal scaler treino', 'expected': 'temporal'},
    {'query': 'Unity Catalog autorização privilégios', 'expected': 'acesso'},
], notas, 2)
print('recall@2=', score, detalhes)

# COMMAND ----------

# MAGIC %md
# MAGIC **Desafio:** acrescente perguntas com sinônimos e sem resposta. Escreva uma resposta manual citando o ID da nota e outra que se abstém por falta de evidência. Um recall alto não comprova qualidade de geração: nenhuma geração ocorreu.
