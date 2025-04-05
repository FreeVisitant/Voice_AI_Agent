import sqlite3
import asyncio
import logging
from typing import Dict, List

logger = logging.getLogger("sqlite_db")
DB_NAME = "leads.db"
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    empresa TEXT NOT NULL,
    necesidades TEXT NOT NULL,
    presupuesto TEXT NOT NULL
);
"""

def init_db() -> None:
    """Inicializa la base de datos y crea la tabla leads si no existe."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(TABLE_SCHEMA)
        conn.commit()
        conn.close()
        logger.info("Base de datos inicializada o ya existente.")
    except Exception as e:
        logger.error("Error al inicializar la base de datos: %s", e)

def insert_lead(lead_info: Dict[str, str]) -> None:
    """Inserta la información del lead en la tabla leads."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO leads (nombre, empresa, necesidades, presupuesto) VALUES (?, ?, ?, ?)",
            (
                lead_info["nombre"],
                lead_info["empresa"],
                lead_info["necesidades"],
                lead_info["presupuesto"],
            ),
        )
        conn.commit()
        conn.close()
        logger.info("Lead insertado correctamente.")
    except Exception as e:
        logger.error("Error al insertar el lead: %s", e)
        raise

def update_lead_field(name: str, field: str, new_value: str) -> None:
    """Actualiza un campo específico de un lead identificado por su nombre."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = f"UPDATE leads SET {field} = ? WHERE nombre = ?"
        cursor.execute(query, (new_value, name))
        conn.commit()
        conn.close()
        logger.info("Lead actualizado correctamente.")
    except Exception as e:
        logger.error("Error al actualizar el lead: %s", e)
        raise

def delete_lead_by_name(name: str) -> None:
    """Elimina un lead de la base de datos según el nombre."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM leads WHERE nombre = ?", (name,))
        conn.commit()
        conn.close()
        logger.info("Lead eliminado correctamente.")
    except Exception as e:
        logger.error("Error al eliminar el lead: %s", e)
        raise

def list_leads() -> List[Dict[str, str]]:
    """Devuelve una lista de todos los leads almacenados."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, empresa, necesidades, presupuesto FROM leads")
        rows = cursor.fetchall()
        conn.close()
        leads = []
        for row in rows:
            leads.append({
                "nombre": row[0],
                "empresa": row[1],
                "necesidades": row[2],
                "presupuesto": row[3]
            })
        return leads
    except Exception as e:
        logger.error("Error al listar los leads: %s", e)
        raise

# Wrappers asíncronos para no bloquear el loop principal

async def async_insert_lead(lead_info: Dict[str, str]) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, insert_lead, lead_info)

async def async_update_lead_field(name: str, field: str, new_value: str) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, update_lead_field, name, field, new_value)

async def async_delete_lead_by_name(name: str) -> None:
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, delete_lead_by_name, name)

async def async_list_leads() -> List[Dict[str, str]]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, list_leads)
