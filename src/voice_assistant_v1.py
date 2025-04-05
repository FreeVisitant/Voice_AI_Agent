import asyncio
import numpy as np
import sounddevice as sd
import os
import logging
from typing import TypedDict

from agents import (
    Agent,
    function_tool,
    set_default_openai_key,
    set_default_openai_api,
)
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    VoicePipeline,
    TTSModelSettings,
    VoicePipelineConfig
)
from config import OPENAI_API_KEY  
from agent.sqlite_db import init_db, async_insert_lead, async_update_lead_field, async_delete_lead_by_name, async_list_leads

set_default_openai_key(OPENAI_API_KEY)  
set_default_openai_api("chat_completions") 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VoiceAssistant")

# Inicializamos la base de datos
init_db()

class LeadInfo(TypedDict):
    nombre: str
    empresa: str
    necesidades: str
    presupuesto: str

class CRMResponse(TypedDict):
    status: str
    message: str

def extract_lead_info(text: str) -> LeadInfo:
    if "Juan" in text:
        return {
            "nombre": "Juan Pérez",
            "empresa": "Empresa XYZ",
            "necesidades": "Servicios de consultoría y software a medida",
            "presupuesto": "10000"
        }
    else:
        return {
            "nombre": "Desconocido",
            "empresa": "Desconocida",
            "necesidades": "No especificadas",
            "presupuesto": "0"
        }

parse_lead_info = function_tool(extract_lead_info)

@function_tool
async def update_crm(lead_info: LeadInfo) -> CRMResponse:
    """Agrega un nuevo lead a la base de datos."""
    logger.info("Actualizando CRM con la siguiente información:")
    logger.info(lead_info)
    try:
        await async_insert_lead(lead_info)
        return {"status": "success", "message": "La información del prospecto se actualizó correctamente."}
    except Exception as e:
        logger.error("Error al actualizar el CRM: %s", e)
        return {"status": "error", "message": "Error al actualizar la información del prospecto."}

@function_tool
async def update_lead_in_db(name: str, field: str, new_value: str) -> CRMResponse:
    """
    Actualiza un campo específico de un lead existente.
    Por ejemplo: actualizar el campo 'empresa' del lead identificado por 'name'.
    """
    logger.info("Actualizando el lead '%s': campo '%s' -> '%s'", name, field, new_value)
    try:
        await async_update_lead_field(name, field, new_value)
        return {"status": "success", "message": f"Lead '{name}' actualizado correctamente."}
    except Exception as e:
        logger.error("Error al actualizar el lead: %s", e)
        return {"status": "error", "message": f"Error al actualizar el lead: {e}"}

@function_tool
async def delete_lead(name: str) -> CRMResponse:
    """Elimina un lead de la base de datos según el nombre."""
    logger.info("Eliminando el lead '%s'", name)
    try:
        await async_delete_lead_by_name(name)
        return {"status": "success", "message": f"Lead '{name}' eliminado correctamente."}
    except Exception as e:
        logger.error("Error al eliminar el lead: %s", e)
        return {"status": "error", "message": f"Error al eliminar el lead: {e}"}

@function_tool
async def list_all_leads() -> str:
    """Devuelve un listado formateado de todos los leads almacenados."""
    logger.info("Listando todos los leads")
    try:
        leads = await async_list_leads()
        if leads:
            response = "\n".join([f"{lead['nombre']} - {lead['empresa']} - {lead['necesidades']} - {lead['presupuesto']}" for lead in leads])
        else:
            response = "No hay leads guardados."
        return response
    except Exception as e:
        logger.error("Error al listar los leads: %s", e)
        return f"Error al listar los leads: {e}"

lead_agent = Agent(
    name="LeadAgent",
    instructions=prompt_with_handoff_instructions("""
Eres un asistente virtual para calificar y gestionar leads.
Recopila información y actualiza el CRM usando:
- 'parse_lead_info' para extraer datos.
- 'update_crm' para agregar nuevos leads.
- 'update_lead_in_db' para modificar campos de un lead existente.
- 'delete_lead' para eliminar un lead por nombre.
- 'list_all_leads' para consultar los leads guardados.
Mantén un tono profesional y amigable.
"""),
    model="gpt-4o",
    tools=[parse_lead_info, update_crm, update_lead_in_db, delete_lead, list_all_leads],
    output_type=str,
)

# Configuración de TTS para una salida de voz natural
tts_settings = TTSModelSettings(
    instructions="Personality: amigable y profesional. Tone: claro y empático. Pronunciation: clara y pausada. Tempo: fluido y un poco más lento. Emotion: cálido."
)

# Función para capturar audio de forma asíncrona 
async def capture_audio(samplerate: float) -> np.ndarray:
    loop = asyncio.get_running_loop()
    recorded_chunks = []

    def callback(indata, frames, time, status):
        if status:
            logger.warning(f"Status de audio: {status}")
        recorded_chunks.append(indata.copy())

    logger.info("Grabando... Por favor, habla ahora.")
    try:
        with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16', callback=callback):
            await loop.run_in_executor(None, input, "Presiona Enter para finalizar la grabación...\n")
    except Exception as e:
        logger.error(f"Error en la captura de audio: {e}")
        return np.array([], dtype=np.int16)
    
    if recorded_chunks:
        return np.concatenate(recorded_chunks, axis=0)
    else:
        return np.array([], dtype=np.int16)

# Asistente de Voz
async def voice_assistant():
    try:
        device_info = sd.query_devices(kind='input')
        samplerate = device_info.get('default_samplerate', 24000)
    except Exception as e:
        logger.error(f"Error al obtener el dispositivo de audio: {e}")
        return

    pipeline_config = VoicePipelineConfig(tts_settings=tts_settings)
    logger.info("Bienvenido al Asistente de Calificación de Leads.")

    while True:
        pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(lead_agent), config=pipeline_config)
        
        cmd = input("Presiona Enter para hablar (o escribe 'esc' para salir): ")
        if cmd.lower() == "esc":
            logger.info("Saliendo del asistente de voz...")
            break

        audio_buffer = await capture_audio(samplerate)
        if audio_buffer.size == 0:
            logger.warning("No se capturó audio. Intenta nuevamente.")
            continue

        audio_input = AudioInput(buffer=audio_buffer)

        try:
            result = await pipeline.run(audio_input)
        except Exception as e:
            logger.error(f"Error durante la ejecución del pipeline: {e}")
            continue

        response_chunks = []
        try:
            async for event in result.stream():
                if event.type == "voice_stream_event_audio":
                    response_chunks.append(event.data)
                elif event.type == "voice_stream_event_lifecycle":
                    logger.info(f"[lifecycle] {event}")
                elif event.type == "voice_stream_event_error":
                    logger.error(f"[error] {event.data}")
        except Exception as e:
            logger.error(f"Error al procesar el stream de eventos: {e}")
            continue

        if response_chunks:
            response_audio = np.concatenate(response_chunks, axis=0)
            logger.info("El asistente está respondiendo...")
            try:
                sd.play(response_audio, samplerate=samplerate)
                sd.wait()
            except Exception as e:
                logger.error(f"Error al reproducir el audio: {e}")
            print("---")
        else:
            logger.warning("No se recibió respuesta de audio. Intenta nuevamente.")

if __name__ == "__main__":
    asyncio.run(voice_assistant())
