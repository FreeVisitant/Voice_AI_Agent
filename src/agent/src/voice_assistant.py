# src/voice_assistant.py
import asyncio
import numpy as np
import sounddevice as sd

from agents import Agent, set_default_openai_key
from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline

set_default_openai_key("YOUR_API_KEY")

voice_system_prompt = """
[Output Structure]
Your output will be delivered in an audio voice response, please ensure that every response meets these guidelines:
1. Use a friendly, human tone that will sound natural when spoken aloud.
2. Keep responses short and segmented—ideally one to two concise sentences per step.
3. Avoid technical jargon; use plain language so that instructions are easy to understand.
4. Provide only essential details so as not to overwhelm the listener.

You are a Lead-Nurturing Assistant. You greet new prospects, gather information about their needs (e.g., name, company, budget, timeline), and respond in a way that feels engaging and helpful.
"""

lead_nurturing_agent = Agent(
    name="LeadNurturingAgent",
    instructions=voice_system_prompt,
    tools=[],
)

# -----------------------------------------------------------------------------
# baseline del asistente
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
            input()  # El usuario pulsa Enter cuando termina de hablar

        # Concatenar los fragmentos de audio en un solo buffer
        recording = np.concatenate(recorded_chunks, axis=0)

        # Crear la entrada de audio para el pipeline
        audio_input = AudioInput(buffer=recording)

        # Ejecuta el pipeline y procesa la respuesta
        result = await pipeline.run(audio_input)

        # Recopilar los fragmentos de audio de la respuesta
        response_chunks = []
        async for event in result.stream():
            if event.type == "voice_stream_event_audio":
                response_chunks.append(event.data)

        # acá vamos a unir la respuesta y reproducirla
        if response_chunks:
            response_audio = np.concatenate(response_chunks, axis=0)
            print("El asistente está respondiendo...")
            sd.play(response_audio, samplerate=samplerate)
            sd.wait()
        else:
            print("No se recibió respuesta de audio.")
        print("---")

# -----------------------------------------------------------------------------
# main del asistente de voz
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(base_voice_assistant())
