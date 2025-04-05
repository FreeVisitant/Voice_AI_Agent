# crm_connector.py

import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AirtableCRM")

class AirtableCRM:
    """
    Módulo para interactuar con Airtable como sistema CRM.
    Requiere:
      - API Key de Airtable
      - Base ID de la base de Airtable
      - Nombre de la tabla (por ejemplo, "Leads")
    """

    def __init__(self, api_key: str, base_id: str, table_name: str):
        self.api_key = api_key
        self.base_id = base_id
        self.table_name = table_name
        self.endpoint = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_lead(self, lead_info: dict) -> dict:
        """
        Crea un nuevo registro en Airtable con la información del lead.
        lead_info debe ser un diccionario con los campos correspondientes.
        """
        data = {"fields": lead_info}
        try:
            response = requests.post(self.endpoint, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info("Lead creado exitosamente.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al crear el lead: {e}")
            return {"error": str(e)}

    def update_lead(self, record_id: str, lead_info: dict) -> dict:
        """
        Actualiza un registro existente en Airtable utilizando el record_id.
        """
        url = f"{self.endpoint}/{record_id}"
        data = {"fields": lead_info}
        try:
            response = requests.patch(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info("Lead actualizado exitosamente.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al actualizar el lead: {e}")
            return {"error": str(e)}

    def get_lead(self, record_id: str) -> dict:
        """
        Obtiene la información de un lead a partir del record_id.
        """
        url = f"{self.endpoint}/{record_id}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info("Lead obtenido exitosamente.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener el lead: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Variables de configuración: definirlas como variables de entorno o directamente aquí
    AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "your_airtable_api_key")
    AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "your_airtable_base_id")
    TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Leads")

    # Inicializa el conector con la configuración
    crm = AirtableCRM(api_key=AIRTABLE_API_KEY, base_id=AIRTABLE_BASE_ID, table_name=TABLE_NAME)
    
    # Ejemplo: Crear un nuevo lead
    new_lead = {
        "Nombre": "Juan Pérez",
        "Empresa": "Empresa XYZ",
        "Necesidades": "Consultoría y desarrollo de software",
        "Presupuesto": "15000"
    }
    
    create_response = crm.create_lead(new_lead)
    logger.info(f"Respuesta al crear lead: {create_response}")
