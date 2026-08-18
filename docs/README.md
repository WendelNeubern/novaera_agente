# Arquitetura

PDF/CSV/DOCX → Python → extração/chunking → busca textual local → Gemini → resposta + fontes.

Esta versão remove OpenAI, PostgreSQL, pgvector e embeddings pagos. A chave Gemini é usada apenas para gerar a resposta final.
