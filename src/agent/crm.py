import requests
import logging
from typing import Dict, Any

logger = logging.getLogger("HubSpotCRMClient")
logger.setLevel(logging.INFO)

class HubSpotCRMClient:
    """
    Cliente para interactuar con el CRM de HubSpot.
    
    Este cliente permite crear o actualizar un contacto en HubSpot utilizando el endpoint
    'createOrUpdate'. Se utiliza un email (generado a partir del nombre si no se proporciona)
    como identificador único del contacto.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.hubapi.com"
    
    def create_or_update_lead(self, lead_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea o actualiza un contacto en HubSpot CRM.
        
        Se espera que lead_info contenga al menos los siguientes campos:
          - nombre
          - empresa
          - necesidades
          - presupuesto
          
        Si no se proporciona un email en lead_info, se genera uno automáticamente.
        
        Parámetros:
            lead_info (dict): Información del lead.
        
        Retorna:
            dict: Resultado de la operación con estado y datos o mensaje de error.
        """
        # Generar un email a partir del nombre si no se especifica
        nombre = lead_info.get("nombre", "desconocido").strip().replace(" ", ".").lower()
        email = lead_info.get("email", f"{nombre}@example.com")
        
        # Construir el endpoint para crear/actualizar el contacto
        endpoint = f"{self.base_url}/contacts/v1/contact/createOrUpdate/email/{email}/"
        params = {"hapikey": self.api_key}
        
        # Construir el payload con las propiedades del contacto
        properties = [
            {"property": "firstname", "value": lead_info.get("nombre", "")},
            {"property": "company", "value": lead_info.get("empresa", "")},
            {"property": "description", "value": lead_info.get("necesidades", "")},
            {"property": "budget", "value": lead_info.get("presupuesto", "")},
        ]
        payload = {"properties": properties}
        
        try:
            response = requests.post(endpoint, params=params, json=payload, timeout=10)
            response.raise_for_status()  # Lanza error si la respuesta no es 2xx
            logger.info(f"Contacto actualizado/creado exitosamente: {response.json()}")
            return {"status": "success", "data": response.json()}
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error: {http_err} - {response.text}")
            return {"status": "error", "message": f"HTTP error: {http_err}"}
        except requests.exceptions.RequestException as err:
            logger.error(f"Network error: {err}")
            return {"status": "error", "message": f"Network error: {err}"}

# Ejemplo de uso y pruebas unitarias simples
if __name__ == "__main__":
    # Reemplaza 'YOUR_HUBSPOT_API_KEY' con tu API key real de HubSpot
    api_key = "YOUR_HUBSPOT_API_KEY"
    crm_client = HubSpotCRMClient(api_key)
    
    # Datos de prueba para un lead
    lead = {
        "nombre": "Juan Pérez",
        "empresa": "Empresa XYZ",
        "necesidades": "Servicios de consultoría y software a medida",
        "presupuesto": "10000"
    }
    
    result = crm_client.create_or_update_lead(lead)
    print(result)
