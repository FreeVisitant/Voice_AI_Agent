import requests  
from agents import function_tool

@function_tool
def store_lead(name: str, company: str, email: str, budget: str, timeline: str) -> dict:
    lead_data = {
        "name": name,
        "company": company,
        "email": email,
        "budget": budget,
        "timeline": timeline,
    }
    
    print("Guardando lead en el CRM:", lead_data)
    return {"status": "success", "message": "Lead guardado exitosamente.", "lead": lead_data}
