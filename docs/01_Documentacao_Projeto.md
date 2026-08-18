# Documentação técnica e funcional

## Finalidade
Agente de IA que responde perguntas exclusivamente com base na documentação fornecida.

## Fluxo
Documento → Python → chunks → embeddings → pgvector.
Pergunta → n8n → FastAPI → busca vetorial → LLM → resposta + fontes.

## Regra de segurança funcional
Se a informação não estiver sustentada pelos documentos recuperados, o agente deve informar que não encontrou a informação.

## Reutilização
A mesma estrutura pode ser aplicada a outras empresas substituindo a pasta `documents`.
