# 🩺 AI Healthcare Triage Assistant (Web-Powered with Grok)

An **AI triage assistant** that:
- Takes symptom input via chat
- Fetches **live data** from **NHS, Mayo Clinic, MedlinePlus**
- Uses **Grok (xAI)** via LangGraph + Guardrails
- Outputs **safe, structured triage advice**
- **Never diagnoses or prescribes**

---

## 🚨 Safety First
- No diagnosis
- No drug names or dosages
- Mandatory disclaimer
- References required
- Hallucination & toxicity filtered

---

## ⚙️ Tech Stack
| Component         | Tool                     |
|------------------|--------------------------|
| UI               | Streamlit                |
| Agent            | LangGraph + LangChain    |
| LLM              | **Grok (xAI)**           |
| Safety           | Guardrails AI            |
| Web Data         | BeautifulSoup + Requests |
| Env              | python-dotenv            |

---

## 🛠️ Setup

```bash
git clone <your-repo-url>
cd healthcare_ai_agent

# Create .env
echo "GROK_API_KEY=your_key_here" > .env

# Install
pip install -r requirements.txt

# Run
streamlit run app.py