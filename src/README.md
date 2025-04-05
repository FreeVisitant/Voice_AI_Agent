# Voice_AI_Agent

## Module Flow Description  
*(Generic and independent descriptions for each module :))*  

---

### `voice_assistant.py`  
This is the most basic version of the voice assistant:

1. **Console Interface**  
   - Interaction occurs through the terminal by pressing *Enter* to start and stop audio recordings.

2. **Audio Capture and Transcription**  
   - Uses the `sounddevice` library to record real-time audio and OpenAI’s SDK to convert speech to text (STT).

3. **Lead Data Extraction**  
   - From the transcribed text, key information (name, company, email, budget, and timeline) is extracted using `extract_lead_info`.

4. **CRM Data Storage**  
   - Once all required fields are collected, the data is saved in the local database using `_store_lead_in_crm`.

5. **Audio Response**  
   - The assistant generates a spoken response and immediately plays it back to the user.

---

### `voice_assistant_v1.py`  
New functionalities compared to the base version (`voice_assistant.py`):

1. **Tool Handling and Type Hinting**  
   - Functions like `extract_lead_info` and `update_crm` are decorated with `@function_tool`, allowing the agent to invoke them in an orderly fashion.  
   - `TypedDict` is used to standardize the structure of lead data and CRM responses.

2. **Logging Integration**  
   - Logging configuration is added to keep track of key events like audio capture or lead submission.

3. **Custom TTS Configuration**  
   - `TTSModelSettings` allows tone and voice style customization. Prompts are adjustable based on agent intent and can be tailored for any agent persona. A generic behavioral prompt can be defined for all user-facing agents, with optional specific prompts.

4. **Asynchronous Audio Capture**  
   - Implements the `capture_audio` function.

5. **Error Handling and Conversation Flow Control**  
   - `logging` and structured events (`voice_stream_event_...`) help control exceptions and provide continuous feedback, reducing ambiguity.

---

### `voice_assistant_v2.py`  
Adds NLP and context features compared to `voice_assistant_v1.py`:

1. **NLP Layer Integration**  
   - Uses `NLPProcessor` from `nlp/entity_intention_extraction.py` to extract entities (manually fixable or context-defined for other LLMs) and classify the user’s intent per transcribed message.

2. **Enhanced Conversation Context**  
   - By detecting intent via a classifier, the agent receives a better context (e.g., qualify leads, answer general database questions, etc.).

---

### `ui_voice_assistant.py`  
Adds a GUI — main differences from `voice_assistant_v2.py`:

1. **Graphical Interface with PySimpleGUI**  
   - Buttons like *“Start Talking”* and *“Stop Recording”* control the audio recording flow.

2. **Database Integration (SQLite)**  
   - Initializes the database at startup (`init_db()`) and uses asynchronous methods (`async_insert_lead`, `async_update_lead_field`, etc.) to handle lead data in the background.

3. **Extra Lead Management Functions**  
   - Besides processing and adding leads, it allows updating specific fields, deleting a lead, and listing all registered entries.

---

## Notes  
Other modules include simple scripts that can be improved. The `config` module defines the environment variable for the API key.

---

### `nlp/entity_intention_extraction.py`  
Handles natural language processing:

1. **Entity Extraction (NER)**  
   - Uses a pipeline based on `dslim/bert-base-NER` to identify names, organizations, and other key elements in the text.

2. **Intent Classification**  
   - Uses a text classification model (`Falconsai/intent_classification`) to detect the user's primary intent (e.g., requesting information, making a purchase, etc.) — a simpler alternative to handing it over directly to the agent.

---

### `agent/sqlite_db.py`  
SQLite database used to store lead information:

1. **Database Initialization**  
   - Creates the `leads` table if it doesn’t exist, ensuring a minimal schema for storing records.

2. **CRUD Operations**  
   - Supports **insert**, **update**, **delete**, and **list** operations.

3. **Wrappers**  
   - Uses asynchronous wrappers to integrate smoothly and non-blockingly with the main voice assistant logic.