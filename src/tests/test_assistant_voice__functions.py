from agent.sqlite_db import DB_NAME
from IPython.display import display, Audio
from agents import Runner, trace
import asyncio
from voice_assistant_v1 import lead_agent  



async def test_queries():
    examples = [
        "Agrega un nuevo lead: Mi nombre es Juan Pérez, trabajo en Empresa XYZ, necesito servicios de consultoría y un presupuesto de 10000.",
        "Actualiza el lead: Carlos Gómez, cambia tu empresa a Empresa ABC.",
        "Elimina el lead de Ana Torres.",
        "Lista todos los leads registrados."
    ]
    with trace("Lead Agent Test"):
        for query in examples:
            result = await Runner.run(lead_agent, query)
            print(f"Usuario: {query}")
            print(result.final_output)
            print("---")
            
asyncio.run(test_queries())

#####ToDo More examples, we need to add. 
display(Audio("voice_agents_audio/account_balance_response_base.mp3"))
display(Audio("voice_agents_audio/product_info_response_base.mp3"))
display(Audio("voice_agents_audio/trending_items_response_base.mp3"))

