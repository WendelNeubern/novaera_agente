# NovaEra Agente IA — Gemini

## 1. Descrição geral

O **NovaEra Agente IA** é um protótipo de agente corporativo de inteligência artificial desenvolvido para responder perguntas com base no conteúdo de documentos da empresa.

A solução foi criada para trabalhar com uma base documental fictícia da empresa **Mercado NovaEra 24h**, permitindo consultar informações institucionais, atendimento ao cliente, trocas e devoluções, perguntas frequentes, compras e fornecedores.

O projeto utiliza **Python** para leitura e processamento dos documentos, uma etapa de **busca local por relevância textual** para localizar os trechos relacionados à pergunta e a **API Gemini** para gerar a resposta final com base nos trechos encontrados.

A solução também possui integração com **n8n**, permitindo utilizar a API Python como parte de um fluxo de automação.

> **Observação:** a base documental utilizada no projeto é fictícia e tem finalidade de demonstração.

---

## 2. Arquitetura da solução

A arquitetura implementada é composta por quatro etapas principais:

```text
                 DOCUMENTOS
              PDF / CSV / DOCX
                     │
                     ▼
              ┌──────────────┐
              │    Python    │
              │  Extração    │
              │ + Chunking   │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ Busca local  │
              │ por termos   │
              │ relevantes   │
              └──────┬───────┘
                     │
              Trechos encontrados
                     │
                     ▼
              ┌──────────────┐
              │ Gemini API   │
              │ Geração da   │
              │ resposta     │
              └──────┬───────┘
                     │
                     ▼
              RESPOSTA + FONTES
```

### Fluxo de uma pergunta

1. O usuário envia uma pergunta para o endpoint `/ask`.
2. A API Python recebe a pergunta.
3. O sistema procura nos documentos carregados os trechos com maior correspondência textual.
4. Os trechos encontrados são enviados como contexto para o modelo Gemini.
5. O Gemini gera uma resposta baseada nesse contexto.
6. A API retorna a resposta e as fontes/documentos encontrados.

### Integração com n8n

O projeto também possui um workflow em `n8n/workflow.json`.

O fluxo é:

```text
Usuário
   │
   ▼
Webhook n8n
   │
   ▼
API Python /ask
   │
   ▼
Busca documental + Gemini
   │
   ▼
Resposta
```

---

## 3. Tecnologias e ferramentas utilizadas

| Tecnologia | Utilização |
|---|---|
| **Python 3.12** | Implementação do agente e processamento dos documentos |
| **FastAPI** | Criação da API HTTP do agente |
| **Google Gemini API** | Geração das respostas |
| **Google GenAI SDK** | Comunicação entre Python e Gemini |
| **pypdf** | Leitura de documentos PDF |
| **python-docx** | Leitura de documentos DOCX |
| **CSV** | Suporte a dados tabulares no processamento documental |
| **n8n** | Orquestração e automação do fluxo |
| **Docker** | Empacotamento e execução da aplicação |
| **Docker Compose** | Inicialização do serviço |
| **Swagger / OpenAPI** | Interface para testar a API em `/docs` |

### Dependências principais

O projeto utiliza, entre outras, as seguintes dependências:

```text
fastapi
uvicorn
pypdf
python-docx
google-genai
pydantic
```

---

## 4. Estrutura do projeto

```text
novaera_agente_gemini/
│
├── documents/
│   └── Documentos utilizados como base de conhecimento
│
├── docs/
│   ├── README.md
│   └── 02_Execucao_Windows.md
│
├── n8n/
│   └── workflow.json
│
├── python/
│   ├── api.py
│   ├── ingest.py
│   ├── rag.py
│   └── document_loader.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 5. Pré-requisitos

Para executar o projeto é necessário ter:

- Windows, Linux ou macOS;
- Docker instalado;
- Docker Compose disponível;
- uma chave da API Gemini.

A chave deve ser configurada no arquivo `.env`.

**Nunca publique o arquivo `.env` no GitHub**, pois ele contém credenciais.

---

## 6. Configuração

Crie o arquivo `.env` a partir do exemplo:

### Windows / PowerShell

```powershell
Copy-Item .env.example .env
```

Depois abra:

```powershell
notepad .env
```

Configure:

```env
GEMINI_API_KEY=sua_chave_da_gemini
GEMINI_MODEL=gemini-3.6-flash
```

A chave deve ser substituída pela sua própria chave da API Gemini.

---

## 7. Execução com Docker

Entre na pasta do projeto:

```powershell
cd C:\Projetos
ovaera_agente_gemini
```

Inicialize a aplicação:

```powershell
docker compose up --build
```

Quando a aplicação estiver disponível, a API poderá ser acessada em:

```text
http://localhost:8000
```

### Verificar a saúde da aplicação

Abra:

```text
http://localhost:8000/health
```

A API deverá retornar uma resposta indicando que está funcionando.

### Interface Swagger

Para testar os endpoints visualmente:

```text
http://localhost:8000/docs
```

---

## 8. Como fazer perguntas ao agente

Na interface Swagger:

1. Acesse `http://localhost:8000/docs`.
2. Localize `POST /ask`.
3. Clique em **Try it out**.
4. Informe a pergunta.
5. Clique em **Execute**.

Exemplo:

```json
{
  "question": "Qual é a política de troca da empresa?",
  "top_k": 5
}
```

O campo `top_k` define a quantidade máxima de trechos considerados pela busca.

---

## 9. Exemplos de perguntas que o agente consegue responder

As perguntas abaixo são exemplos compatíveis com a base documental fictícia utilizada no projeto.

### Informações institucionais

```text
Qual é o segmento de atuação do Mercado NovaEra 24h?
```

```text
Qual é a missão da empresa?
```

```text
Quais são os valores do NovaEra?
```

```text
Quais são os objetivos estratégicos da empresa?
```

### Atendimento

```text
A loja funciona 24 horas?
```

```text
Quais formas de pagamento são aceitas?
```

```text
Como faço uma reclamação?
```

```text
Quais são os canais de atendimento do NovaEra?
```

### Trocas e devoluções

```text
Qual é o prazo para troca de produtos com vício?
```

```text
Qual é o prazo para troca de eletroportáteis?
```

```text
Como funciona a troca de produtos in natura?
```

### Reembolsos

```text
Qual é o prazo para reembolso via PIX?
```

```text
Qual é o prazo de reembolso no cartão de crédito?
```

### Programa NovaEra+

```text
Como faço para participar do NovaEra+?
```

```text
Como acumulo pontos no NovaEra+?
```

```text
Os pontos do NovaEra+ podem ser transferidos?
```

```text
Quais são os níveis do NovaEra+?
```

### Compras e fornecedores

```text
Quais são os critérios utilizados para avaliar fornecedores?
```

```text
Quem aprova uma compra de até R$ 10 mil?
```

```text
Quem aprova uma compra acima de R$ 200 mil?
```

```text
Qual é a meta de OTIF dos fornecedores?
```

---

## 10. Exemplos de respostas geradas

Os exemplos abaixo representam o tipo de resposta esperado a partir dos documentos da base.

### Exemplo 1 — Trocas

**Pergunta:**

```text
Qual é o prazo para troca de eletroportáteis?
```

**Resposta esperada:**

```text
O prazo para troca de utensílios e eletroportáteis em caso de vício é de até 90 dias,
observando as condições de garantia e a documentação aplicável.
```

**Fonte:**

```text
Política de Atendimento, Trocas, Devoluções e Privacidade
```

---

### Exemplo 2 — Reembolso

**Pergunta:**

```text
Qual é o prazo para reembolso via PIX?
```

**Resposta esperada:**

```text
O reembolso via PIX pode ocorrer em até 24 horas úteis após a conferência.
```

**Fonte:**

```text
Política de Atendimento, Trocas, Devoluções e Privacidade
```

---

### Exemplo 3 — Programa de fidelidade

**Pergunta:**

```text
Os pontos do NovaEra+ podem ser transferidos para outra pessoa?
```

**Resposta esperada:**

```text
Não. Os pontos do NovaEra+ estão vinculados ao CPF do titular e não podem
ser transferidos para outra pessoa.
```

**Fonte:**

```text
Manual de Perguntas Frequentes (FAQ)
```

---

### Exemplo 4 — Fornecedores

**Pergunta:**

```text
Qual é a meta de OTIF dos fornecedores?
```

**Resposta esperada:**

```text
A meta de OTIF estabelecida para os fornecedores é superior a 95%.
```

**Fonte:**

```text
Manual de Fornecedores e Política de Compras
```

---

### Exemplo 5 — Alçada de aprovação

**Pergunta:**

```text
Quem aprova uma compra acima de R$ 200 mil?
```

**Resposta esperada:**

```text
Compras acima de R$ 200 mil dependem de aprovação da Diretoria responsável
e da área de Compras.
```

**Fonte:**

```text
Manual de Fornecedores e Política de Compras
```

---

## 11. Teste de ausência de informação

Uma característica importante do agente é evitar que informações sejam inventadas quando elas não estão disponíveis na documentação.

Por exemplo:

```text
Quantos funcionários o Mercado NovaEra possui?
```

Caso essa informação não esteja nos documentos carregados, o comportamento esperado é:

```text
Não encontrei essa informação nos documentos disponíveis.
```

Esse teste é importante para demonstrar o comportamento do agente diante de perguntas que estão fora da base de conhecimento.

---

## 12. Recarregar os documentos

Os documentos ficam na pasta:

```text
documents/
```

Para adicionar novos documentos, coloque-os nessa pasta.

A API possui o endpoint:

```text
POST /reload
```

que permite recarregar os documentos sem alterar o código da aplicação.

---

## 13. API principal

### `GET /health`

Verifica se a API está funcionando.

### `GET /documents`

Lista os documentos carregados e a quantidade de trechos indexados.

### `POST /reload`

Reprocessa os documentos existentes na pasta `documents`.

### `POST /ask`

Recebe uma pergunta e retorna a resposta gerada pelo agente.

Exemplo:

```json
{
  "question": "Qual é a missão da empresa?",
  "top_k": 5
}
```

Resposta:

```json
{
  "answer": "Resposta baseada no conteúdo documental...",
  "sources": [
    {
      "document": "documento.pdf",
      "page": 1,
      "row": null,
      "score": 0.4
    }
  ]
}
```

---

## 14. Limitações da versão atual

Esta versão foi projetada como um **MVP funcional**.

A recuperação dos documentos utiliza uma busca textual local baseada na correspondência entre os termos da pergunta e os trechos dos documentos. Portanto, perguntas muito diferentes da linguagem utilizada na documentação podem recuperar menos contexto.

Uma evolução futura poderá substituir ou complementar essa busca por:

- embeddings locais;
- busca semântica;
- banco vetorial;
- reranking;
- controle de acesso por usuário;
- autenticação;
- interface web de chat;
- histórico de conversas;
- observabilidade;
- ingestão automatizada de documentos;
- integração ampliada com n8n.

---

## 15. Objetivo de reutilização

O projeto foi estruturado para servir como uma base para outros projetos de agentes corporativos.

Para utilizar uma nova empresa ou uma nova base de conhecimento, a pasta `documents/` pode receber novos documentos, mantendo a mesma estrutura geral da aplicação.

O agente pode, dessa forma, ser adaptado para diferentes áreas organizacionais, como:

- RH;
- Financeiro;
- Jurídico;
- Compras;
- Operações;
- Atendimento;
- Estratégia.

---

## 16. Licença

Projeto desenvolvido para fins de demonstração, estudo e prototipação de agentes corporativos de inteligência artificial.
