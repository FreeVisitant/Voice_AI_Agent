import re
import json

def extract_lead_info(text: str) -> dict:
    """
    Extrae información del lead de un string.
    Primero intenta parsear el texto como JSON.
    Si falla, utiliza expresiones regulares simples para extraer:
      - name: se espera el formato "Name: <valor>"
      - company: "Company: <valor>"
      - email: se detecta un email
      - budget: "Budget: <valor>" (ej. $500)
      - timeline: "Timeline: <valor>"
    """
    try:
        data = json.loads(text)
        required_keys = ["name", "company", "email", "budget", "timeline"]
        if all(key in data for key in required_keys):
            return data
    except Exception:
        pass

    lead_info = {}

    # Extraer email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        lead_info["email"] = email_match.group(0)

    # Extraer nombre (buscando un patrón tipo "Name: ...")
    name_match = re.search(r'Name[:\s]+([\w\s]+)', text, re.IGNORECASE)
    if name_match:
        lead_info["name"] = name_match.group(1).strip()

    # Extraer empresa
    company_match = re.search(r'Company[:\s]+([\w\s]+)', text, re.IGNORECASE)
    if company_match:
        lead_info["company"] = company_match.group(1).strip()

    # Extraer presupuesto
    budget_match = re.search(r'Budget[:\s]+([$€]\d+)', text, re.IGNORECASE)
    if budget_match:
        lead_info["budget"] = budget_match.group(1).strip()

    # Extraer timeline
    timeline_match = re.search(r'Timeline[:\s]+([\w\s]+)', text, re.IGNORECASE)
    if timeline_match:
        lead_info["timeline"] = timeline_match.group(1).strip()

    return lead_info