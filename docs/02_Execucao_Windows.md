# Execução no Windows

1. Extraia o ZIP.
2. Abra PowerShell na pasta.
3. Crie `.env`:
```powershell
Copy-Item .env.example .env
notepad .env
```
4. Preencha:
```env
GEMINI_API_KEY=sua_chave
GEMINI_MODEL=gemini-2.5-flash
```
5. Execute:
```powershell
docker compose up --build
```
6. Teste `http://localhost:8000/health`.
7. Abra `http://localhost:8000/docs` e use `POST /ask`.
A API carrega os documentos automaticamente; não é necessário executar `python ingest` nem PostgreSQL.
