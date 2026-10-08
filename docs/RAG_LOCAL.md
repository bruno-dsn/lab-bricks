# RAG local: contrato, evidência e resultado negativo

O app usa uma resposta extrativa: recupera e apresenta trechos com IDs, ou se abstém quando nenhum score supera o limiar. Isso não é geração por LLM. O notebook 16 contém essa prática e o benchmark.

## Geração que foi executada

Sete casos congelados em rag_protocol.json foram executados com Qwen2.5-0.5B-Instruct Q4_K_M e llama.cpp b11429, commit d81235049. Pesos: revisão 9217f5db79a29953eb74d5343926648285ec7e67; SHA do arquivo registrado. Temperatura 0, seed 42, contexto 4096, dois threads CPU e até 360 tokens por caso.

Resultado de rag_results.json: sete contratos rejeitados, sete abstenções normalizadas, zero respostas úteis aceitas e 3.150 tokens totais. Foram encontradas contradições, como abstenção acompanhada de citações. O protocolo deliberadamente usou limiar de recuperação zero para expor evidência fraca. Não é configuração recomendada.

O validador exige JSON com resposta, citacoes e absteve. Citações devem existir no contexto; uma abstenção não cita uma resposta. Um contrato válido ainda pode conter afirmações sem suporte: avaliação factual permanece pendente e separada da validação estrutural. Output bruto, latência e recuperação são registrados por caso.

## Reprodução opcional

```bash
python scripts/baixar_modelos.py qwen --destino ../modelos-lab/qwen
python scripts/evaluate_rag.py --help
```

Obtenha llama.cpp b11429 na [release oficial](https://github.com/ggml-org/llama.cpp/releases/tag/b11429). Use o binário apropriado ao seu sistema e confira versão e procedência. A execução registrada foi Linux x86_64; o pacote oficial linux-x64 teve SHA f6d25dde8f51133143d1453da4fd5f73b145127177612a283bf7995957af3392. O binário não é incluído no laboratório.

```bash
python scripts/evaluate_rag.py --model-path ../modelos-lab/qwen/qwen2.5-0.5b-instruct-q4_k_m.gguf --server-bin /caminho/llama-server
```

O script inicia e encerra seu próprio servidor em localhost, recusa porta ocupada, confere modelo e versão, não oferece ferramentas e limita contexto/saída. Texto recuperado é dado não confiável. Essas medidas não garantem resistência universal a prompt injection.

## Custo e critério de avanço

Não foi inventado preço para CPU local. O relatório guarda latência e tokens; custo monetário fica nulo. Se souber seu preço horário, informe --preco-cpu-hora para estimar latência/3600 vezes preço. A estimativa não inclui aquisição de hardware, ociosidade ou carregamento.

O próximo experimento precisa registrar uma hipótese, novos pesos/engine, hashes e critério de suporte factual antes de executar. Compare utilidade, abstenção correta, citações, segurança e custo. Não transforme sete falhas em uma afirmação de qualidade.
