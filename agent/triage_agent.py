# agent/triage_agent.py
import json
import re
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.prompts import ChatPromptTemplate
from .web_fetcher import fetch_medical_data  # optional

llm = Ollama(model="phi3", temperature=0.3)

triage_prompt = ChatPromptTemplate.from_template("""
You are a friendly, safe AI healthcare triage assistant.

Your task is to analyze the user's described symptoms or health query and return a structured JSON response.

User symptoms or question:
{symptoms}

Available web information:
{web_data}

Respond strictly in JSON with the following fields:
{{ 
  "Summary": "One concise paragraph summarizing the possible context or concern.",
  "Possible_Causes": ["Possible cause 1", "Possible cause 2"],
  "Triage_Recommendation": "One of ['Self-Care', 'See Doctor Soon', 'Urgent GP', 'Emergency']",
  "Next_Steps": ["Step 1", "Step 2"],
  "Disclaimer": "This is not medical advice. Consult a doctor.",
  "References": [
      {{"name": "NHS - Fever", "url": "https://www.nhs.uk/conditions/fever"}},
      {{"name": "Mayo Clinic - Fatigue", "url": "https://www.mayoclinic.org/diseases-conditions/fatigue"}}
  ]
}}

If the query is unrelated to health, respond with:
{{ 
  "Summary": "This triage assistant cannot answer questions unrelated to health.",
  "Possible_Causes": [],
  "Triage_Recommendation": "N/A",
  "Next_Steps": [],
  "Disclaimer": "This is not medical advice. Consult a healthcare provider for real symptoms.",
  "References": []
}}
""")

def clean_json_output(text: str):
    """Removes markdown code fences and extracts JSON cleanly."""
    # Remove Markdown code blocks
    text = re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    # Extract JSON content if embedded
    json_match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if json_match:
        text = json_match.group(0)
    return text

def run_triage_agent(symptoms: str):
    """Runs the healthcare triage model and returns structured output."""
    try:
        web_data = fetch_medical_data(symptoms)
    except Exception:
        web_data = "Information unavailable"

    chain_triage = triage_prompt | llm
    result_raw = chain_triage.invoke({
        "symptoms": symptoms,
        "web_data": web_data or "No web data found."
    })

    # Clean and parse JSON
    cleaned_result = clean_json_output(result_raw)
    try:
        result_json = json.loads(cleaned_result)
    except json.JSONDecodeError:
        result_json = {"Summary": result_raw}

    return result_json
