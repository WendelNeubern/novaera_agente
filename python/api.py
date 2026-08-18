from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from .rag import ingest,search,answer,INDEX
app=FastAPI(title="NovaEra AI Agent - Gemini",version="1.0")
class Question(BaseModel):
    question:str
    top_k:int=5
@app.on_event("startup")
def startup(): ingest("documents")
@app.get("/health")
def health(): return {"status":"ok","engine":"local-search + Gemini"}
@app.get("/documents")
def documents():
    from .rag import INDEX
    return {"documents":sorted(set(x["document"] for x in INDEX)),"chunks":len(INDEX)}
@app.post("/reload")
def reload(): return ingest("documents")
@app.post("/ask")
def ask(q:Question):
    if not q.question.strip(): raise HTTPException(400,"Informe uma pergunta.")
    s=search(q.question,max(1,min(q.top_k,10)))
    return {"answer":answer(q.question,s),
            "sources":[{"document":x["document"],"page":x["page"],"row":x["row"],"score":x["score"]} for x in s]}
