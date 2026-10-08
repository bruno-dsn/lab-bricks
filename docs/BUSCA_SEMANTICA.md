# Busca lexical e semântica: medir antes de recomendar

O benchmark da 2.1 foi preservado: 30 paráfrases e seis perguntas fora do escopo. O corpus de 35 aulas foi congelado antes das 10 aulas novas. A busca interativa pode usar 45 aulas; seus resultados não devem ser confundidos com a medição congelada.

## Protocolo e resultados

search_protocol.json guarda hashes das perguntas e do corpus. O script recusa divergência. TF-IDF usa documentos; o encoder local usa chunks de 850 caracteres e sobreposição de 120, com título. Ranking semântico calcula produto escalar entre vetores normalizados e mantém documentos únicos.

| Medida | TF-IDF | Semântica |
|---|---:|---:|
| Recall@1 | 46,7% | 40,0% |
| Recall@3 | 73,3% | 63,3% |
| MRR@5 | 0,602 | 0,529 |
| Cobertura com limiar | 16,7% | 76,7% |
| Acerto entre cobertas | 80,0% | 39,1% |
| Abstenção fora do escopo | 66,7% | 100,0% |

Limiares fixados em 0,12 e 0,45. Foram definidos antes da medição, sem calibração estatística. Similaridade não é probabilidade. A cobertura maior veio com menor precisão. Encoder e chunking mudaram juntos; este experimento não isola a causa da diferença.

## Modelo e reprodução opcional

Xenova/paraphrase-multilingual-MiniLM-L12-v2, revisão 2c4055b12046f11709e9df2c122e59ffbdc2f900. ONNX e tokenizer têm SHA verificado, execução CPU com dois threads, pooling por máscara e normalização L2. Vetores têm 384 dimensões.

```bash
python -m pip install -r requirements-semantica.txt
python scripts/baixar_modelos.py encoder --destino ../modelos-lab/encoder
python scripts/evaluate_search.py --model-dir ../modelos-lab/encoder
python scripts/buscar_semantica.py --model-dir ../modelos-lab/encoder "Como evitar somar a mesma venda duas vezes?"
```

Os downloads são explícitos e ficam fora do repositório. O pacote traz um cache pequeno com vetores das perguntas congeladas; ele não transforma uma pergunta nova em vetor. Para busca livre, execute o encoder. Cache é NPZ sem pickle, com hash, dimensão e texto conferidos.

## Prática

Escolha cinco falhas em search_results.json. Compare a intenção da pergunta, o esperado e os documentos recuperados. Depois congele outro conjunto independente para testar uma hipótese: chunking igual, outro encoder ou ajuste de limiar em conjunto separado. Não reescreva o benchmark existente para melhorar a nota.
