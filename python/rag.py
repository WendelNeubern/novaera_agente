import os,re
from pathlib import Path
from .document_loader import load_file

INDEX=[]
def chunks(text,size=1200,overlap=150):
    r=[]; s=0
    while s<len(text):
        e=min(len(text),s+size); r.append(text[s:e])
        if e==len(text): break
        s=e-overlap
    return r

def norm(t): return re.sub(r"\s+"," ",t.lower()).strip()

def ingest(directory="documents"):
    global INDEX
    INDEX=[]
    files=[p for p in Path(directory).glob("*") if p.suffix.lower() in {".pdf",".csv",".docx"}]
    total=0
    for path in files:
        for item in load_file(str(path)):
            for piece in chunks(item["text"]):
                INDEX.append({"document":path.name,"content":piece,"page":item.get("page"),
                              "row":item.get("row"),"tokens":set(norm(piece).split())})
                total+=1
    return {"documents":len(files),"chunks":total}

def search(question,k=5):
    if not INDEX: ingest()
    q=set(norm(question).split()); scored=[]
    for x in INDEX:
        common=len(q & x["tokens"])
        if common: scored.append((common/max(1,len(q)),x))
    scored.sort(key=lambda x:x[0],reverse=True)
    return [{"document":x["document"],"content":x["content"],"page":x["page"],
             "row":x["row"],"score":round(s,4)} for s,x in scored[:k]]

def answer(question,sources):
    if not sources: return "Não encontrei essa informação nos documentos disponíveis."
    key=os.getenv("GEMINI_API_KEY")
    if not key:
        return "GEMINI_API_KEY não configurada. Trechos encontrados:\n\n" + \
               "\n\n".join(f"[{x['document']}]\n{x['content']}" for x in sources)
    from google import genai
    client=genai.Client(api_key=key)
    context="\n\n".join(f"[Fonte: {x['document']}]\n{x['content']}" for x in sources)
    prompt=f"""Você é um agente corporativo de consulta documental.
Responda SOMENTE com informações sustentadas pelo CONTEXTO.
Não invente informações. Se não houver suporte suficiente, diga:
"Não encontrei essa informação nos documentos disponíveis."
Seja objetivo e informe as fontes utilizadas.

CONTEXTO:
{context}

PERGUNTA:
{question}"""
    return client.models.generate_content(
        model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"), contents=prompt
    ).text
