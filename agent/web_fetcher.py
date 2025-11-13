# agent/web_fetcher.py
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from .utils import clean_text

def fetch_medical_data(symptom: str) -> dict:
    """
    Fetch and summarize medical data from trusted sites (NHS, Mayo Clinic, MedlinePlus).
    Returns both the summary text and structured references.
    """
    query = symptom.replace(" ", "+")
    search_urls = {
        "NHS": f"https://www.nhs.uk/search/?q={query}",
        "Mayo Clinic": f"https://www.mayoclinic.org/search/search-results?q={query}",
        "MedlinePlus": f"https://medlineplus.gov/search?q={query}"
    }

    raw_texts = {}
    headers = {"User-Agent": "Mozilla/5.0 (compatible; HealthcareTriageBot/1.0)"}

    for site, url in search_urls.items():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "lxml")
            paragraphs = soup.find_all("p")
            text = " ".join([clean_text(p.get_text()) for p in paragraphs[:10]])
            if text:
                raw_texts[site] = text
        except Exception as e:
            print(f"Error fetching {site}: {e}")
            continue

    if not raw_texts:
        return {"summary": "No reliable web data found.", "references": []}

    # Combine all text for summarization
    combined_text = " ".join(raw_texts.values())[:10000]

    # Use local Ollama model (no API key)
    llm = OllamaLLM(model="phi3", temperature=0.3)

    prompt = PromptTemplate.from_template("""
    You are a medical research assistant.
    Summarize the following content focusing only on:
    - Common causes
    - Red flag symptoms
    - When to seek urgent care
    - Self-care advice (non-medical)

    DO NOT diagnose, prescribe, or recommend drugs.

    Content:
    {text}

    Summary:
    """)

    try:
        response = llm.invoke(prompt.format(text=combined_text))
        summary = response if isinstance(response, str) else response.content
    except Exception as e:
        print(f"Error summarizing text: {e}")
        summary = "Summary unavailable due to processing error."

    # Create clickable hyperlinks for sources
    references = [
        {"name": name, "url": url}
        for name, url in search_urls.items() if name in raw_texts
    ]

    return {
        "summary": summary,
        "references": references
    }


def summarize_with_ollama(text: str) -> str:
    """Use local Ollama model to summarize safely."""
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import PromptTemplate

    llm = OllamaLLM(model="phi3", temperature=0.3)

    prompt = PromptTemplate.from_template("""
    You are a healthcare assistant.
    Summarize this text into key insights:
    - Possible causes
    - When to seek urgent care
    - Self-care advice (no medications or dosages)

    Text:
    {text}

    Summary:
    """)

    try:
        # Run the LLM
        result = llm.invoke(prompt.format(text=text))

        # If it’s a dict or has .content, handle gracefully
        if isinstance(result, dict):
            return result.get("content", str(result))
        elif hasattr(result, "content"):
            return result.content
        else:
            return str(result)

    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Summary unavailable."

