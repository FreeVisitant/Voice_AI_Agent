# Voice_AI_Agent

**Descripción:** El proyecto consiste en un asistente de voz basado que interactúa con una base de datos y además hace uso de técnicas de Procesamiento de Lenguaje Natural. El objetivo principal es recibir comandos por voz, extraer información relevante (entidades e intenciones), y luego integrarse con una base de datos o con un CMR para facilitar la gestión de leads, clientes o datos relevantes para distintos tipos de negocio.

### Instalación de Dependencias

Para instalar las dependencias que necesitarás para ejecutar el asistente, copia el siguiente comando en tu consola y córrelo:

```bash
pip install -r requirements.txt
```

## Frameworks(Stack) utilizado:

1. **Python 3.13.2**  
   - Lenguaje usado.

2. **openai-agents[voice]**  
   - **SDK de OpenAI:** código abierto, ligero. Lo uso para construir y orquestar flujos de trabajo entre diversos agentes que se pueden incorporar.

3. **numpy**  
   - Todos amamos a numpy.

4. **sounddevice**  
   - Para la grabación y reproducción de audio a través de matrices de NumPy.

5. **openai**  
   - Biblioteca oficial de OpenAI para integrar modelos y servicios disponibles mediante la API.

6. **python-dotenv**  
   - Carga variables de entorno desde archivos `.env` para configuraciones seguras. (Recomiendo la creación local del .env a la hora de probar el proyecto donde guarden la OpenAI-API-key(recuerden excluir en el gitnore)).

8. **transformers**  
   - ​La biblioteca Transformers de Hugging Face donde podemos usar al grandioso Bert y su familia :).

9. **PySimpleGUI**  
   - Librería para crear interfaces gráficas para gente que no les gustan las interfaces gráficas, la lectura directa del código de máquina está infravalorada :).


> **Nota:** Para PySimpleGUI, en caso de tener problema con la importación de algún módulo tipo Text intenta:
> ```bash
> pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
> ```

## Estructura del Proyecto

La estructura principal del repositorio es la siguiente:

```
|-- Voice_AI_Agent
    |-- .gitignore
    |-- LICENSE
    |-- README.md
    |-- leads.db
    |-- requirements.txt
    |-- src (lógica principal)
    |   |-- config.py (variables de entorno leídas con `python-dotenv`)
    |   |-- ui.py (versión con la GUI integrada)
    |   |-- voice_assistant.py (versión base, interacción directa con consola, sin análisis de intención complejo)
    |   |-- voice_assistant_v1.py (versión media, interacción por con consola, manejo de sqlite, sin análisis de intención complejo)
    |   |-- voice_assistant_v2.py (versión avanzada, interacción por con consola, manejo de sqlite, análisis de intención complejo (con modelos de Hugging Face))
    |   |-- agent
    |   |   |-- crm.py
    |   |   |-- crm_connector.py
    |   |   |-- crm_integration.py (intento de integración con un CRM(intento fallido) al igual que el resto)
    |   |   |-- sqlite_db.py (Trabajo con `SQLite` local (`leads.db`).)
    |   |-- nlp
    |   |   |-- entity_extraction.py (extracción rústica :())
    |   |   |-- entity_intention_extraction.py (Lógica para el uso de modelos para la clasificación de textos(análisis de sentimientos).)
    |   |-- tests
    |   |-- api
    |       |-- __pycache__
    |-- .git
```

