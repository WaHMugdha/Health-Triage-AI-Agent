import re
from typing import Dict, Any

def clean_text(text: str) -> str:
    """Remove extra whitespace and clean scraped text."""
    return re.sub(r'\s+', ' ', text).strip()

def extract_references(text: str) -> str:
    """Extract source references from web content."""
    sources = []
    if "nhs.uk" in text.lower():
        sources.append("NHS.uk")
    if "mayoclinic.org" in text.lower():
        sources.append("Mayo Clinic")
    if "medlineplus.gov" in text.lower():
        sources.append("MedlinePlus")
    return ", ".join(sources) if sources else "Trusted medical websites"