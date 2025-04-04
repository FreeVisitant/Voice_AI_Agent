import requests  
from agents import function_tool

def _store_lead_in_crm(name: str, company: str, email: str, budget: str, timeline: str) -> dict:
    lead_data = {
        "name": name,
        "company": company,
        "email": email,
        "budget": budget,
        "timeline": timeline,
    }
    print("Guardando lead en el CRM (función pura):", lead_data)
    return {"status": "success", "message": "Lead guardado exitosamente.", "lead": lead_data}

@function_tool
def store_lead(name: str, company: str, email: str, budget: str, timeline: str) -> dict:
    return _store_lead_in_crm(name, company, email, budget, timeline)