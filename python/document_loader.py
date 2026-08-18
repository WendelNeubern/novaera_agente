from pathlib import Path
import csv

def load_pdf(path):
    import pypdf
    reader=pypdf.PdfReader(path)
    return [{"text":(p.extract_text() or "").strip(),"page":i,"row":None}
            for i,p in enumerate(reader.pages,1) if (p.extract_text() or "").strip()]

def load_csv(path):
    out=[]
    with open(path,encoding="utf-8-sig",newline="") as f:
        for i,row in enumerate(csv.DictReader(f),2):
            text=" | ".join(f"{k}: {v}" for k,v in row.items() if v not in (None,""))
            if text.strip(): out.append({"text":text,"page":None,"row":i})
    return out

def load_docx(path):
    from docx import Document
    doc=Document(path)
    return [{"text":p.text.strip(),"page":None,"row":None} for p in doc.paragraphs if p.text.strip()]

def load_file(path):
    ext=Path(path).suffix.lower()
    if ext==".pdf": return load_pdf(path)
    if ext==".csv": return load_csv(path)
    if ext==".docx": return load_docx(path)
    raise ValueError(f"Formato não suportado: {ext}")
