import asyncio
import numpy as np
import sounddevice as sd

from agents import Agent, set_default_openai_key
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline
from agent.crm_integration import store_lead, _store_lead_in_crm
from config import OPENAI_API_KEY
from nlp.entity_extraction import extract_lead_info

set_default_openai_key(OPENAI_API_KEY)


voice_system_prompt = """
[Output Structure]
Your output will be delivered in an audio voice response, please ensure that every response meets these guidelines:
1. Use a friendly, human tone that will sound natural when spoken aloud.
2. Keep responses short and segmented—ideally one to two concise sentences per step.
3. Avoid technical jargon; use plain language so that instructions are easy to understand.
4. Provide only essential details so as not to overwhelm the listener.

You are a Lead-Nurturing Assistant. Your tasks are:
- Greet the prospect warmly.
- Ask for the prospect's name, company, email, budget, and timeline.
- If any information is missing or ambiguous, ask for clarification.
- Once all necessary data is gathered, confirm the information with the prospect.
- Finally, store the lead information in the CRM using the provided tool.
"""


lead_nurturing_agent = Agent(
    name="LeadNurturingAgent",
    instructions=voice_system_prompt,
    tools=[store_lead],  # Para que el agente pueda usar store_lead si hace function calling
)

# -----------------------------------------------------------------------------
# BSELINE DEL ASISTENTE DE VOZ
# -----------------------------------------------------------------------------
async def base_voice_assistant():
    samplerate = sd.query_devices(kind='input')['default_samplerate']
    print("Voice assistant iniciado. Presiona Enter para hablar o escribe 'esc' para salir.")

    # Creamos un pipeline apuntando a nuestro agente de leads
    pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(lead_nurturing_agent))

    while True:
        cmd = input("Presiona Enter para hablar (o escribe 'esc' para salir): ")
        if cmd.lower() == "esc":
            print("Saliendo del asistente de voz...")
            break

        print("Escuchando... Presiona Enter nuevamente para finalizar grabación.")
        recorded_chunks = []

        # Captura de audio desde el micrófono
        with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16',
                            callback=lambda indata, frames, time, status: recorded_chunks.append(indata.copy())):
            input()  # Pulsa Enter cuando termines de hablar

        if not recorded_chunks:
            print("No se grabó audio. Intenta hablar antes de presionar Enter.")
            continue

        # Concatenar los fragmentos de audio en un solo buffer
        recording = np.concatenate(recorded_chunks, axis=0)

        # Crear la entrada de audio para el pipeline (aquí se usará Whisper internamente)
        audio_input = AudioInput(buffer=recording)

        # Ejecuta el pipeline y procesa la respuesta
        result = await pipeline.run(audio_input)

        # Intentamos obtener el transcript textual (generado por Whisper a través del SDK)
        if hasattr(result, "get_transcript"):
            transcript = result.get_transcript()
        else:
            transcript = """
            Name: John Doe
            Company: Acme Corp
            Email: john.doe@acme.com
            Budget: $1000
            Timeline: Next quarter
            """
        print("Transcript obtenido:")
        print(transcript)

        # Extraemos la información del lead del transcript
        lead_data = extract_lead_info(transcript)
        print("Datos extraídos del lead:", lead_data)

        # Si se tienen todos los datos necesarios, se almacena el lead en el CRM
        required_keys = ["name", "company", "email", "budget", "timeline"]
        if all(key in lead_data for key in required_keys):
            # Usamos la función pura
            store_result = _store_lead_in_crm(
                name=lead_data["name"],
                company=lead_data["company"],
                email=lead_data["email"],
                budget=lead_data["budget"],
                timeline=lead_data["timeline"]
            )
            print("Resultado del almacenamiento del lead:", store_result)
        else:
            print("Información incompleta para almacenar el lead.")

        # Recopilar los fragmentos de audio de la respuesta del agente
        response_chunks = []
        async for event in result.stream():
            if event.type == "voice_stream_event_audio":
                response_chunks.append(event.data)

        # Unir la respuesta y reproducirla
        if response_chunks:
            response_audio = np.concatenate(response_chunks, axis=0)
            print("El asistente está respondiendo...")
            sd.play(response_audio, samplerate=samplerate)
            sd.wait()
        else:
            print("No se recibió respuesta de audio.")
        print("---")




if __name__ == "__main__":
    asyncio.run(base_voice_assistant())
