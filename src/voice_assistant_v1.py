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

set_default_openai_key(OPENAI_API_KEY)  
set_default_openai_api("chat_completions") 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VoiceAssistant")

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
def update_crm(lead_info: LeadInfo) -> CRMResponse:
    logger.info("Actualizando CRM con la siguiente información:")
    logger.info(lead_info)
    return {"status": "success", "message": "La información del prospecto se actualizó correctamente."}

lead_agent = Agent(
    name="LeadAgent",
    instructions=prompt_with_handoff_instructions("""
Eres un asistente virtual para calificar leads. Recopila la información del prospecto y actualiza el CRM.
Utiliza 'parse_lead_info' para extraer datos y 'update_crm' para actualizar la información.
Mantén un tono profesional y amigable.
"""),
    model="gpt-4o",
    tools=[parse_lead_info, update_crm],
    output_type=str,
)

# Config de TTS para una salida de voz natural
tts_settings = TTSModelSettings(
    instructions="Personality: amigable y profesional. Tone: claro y empático. Pronunciation: clara y pausada. Tempo: fluido y un poco más lento. Emotion: cálido."
)

# func para capturar audio de forma asíncrona 
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
            # Usamos run_in_executor para no bloquear el loop
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

        # Ejecuta el pipeline de voz
        try:
            result = await pipeline.run(audio_input)
        except Exception as e:
            logger.error(f"Error durante la ejecución del pipeline: {e}")
            continue

        # Recolecta y reproduce la respuesta de audio
        response_chunks = []
        try:
            async for event in result.stream():
                if event.type == "voice_stream_event_audio":
                    response_chunks.append(event.data)
                elif event.type == "voice_stream_event_lifecycle":
                    # Se imprime el evento completo para evitar error al acceder a un atributo inexistente
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
