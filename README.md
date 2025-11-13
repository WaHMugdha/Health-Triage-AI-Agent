# AI Healthcare Triage Assistant (Web-Powered with Grok)

An **AI triage assistant** that:
- Takes symptom input via chat
- Fetches **live data** from **NHS, Mayo Clinic, MedlinePlus**
- Uses Ollama
- Outputs **safe, structured triage advice**
- **Never diagnoses or prescribes**

---

## Safety First
- No diagnosis
- No drug names or dosages
- Mandatory disclaimer
- References required
- Hallucination & toxicity filtered

---

## Tech Stack
| Component         | Tool                     |
|------------------|--------------------------|
| UI               | Streamlit                |
| Agent            | LangGraph + LangChain    |
| LLM              | Ollama                   |
| Safety           | Guardrails AI            |
| Web Data         | BeautifulSoup + Requests |
| Env              | python-dotenv            |

