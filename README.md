# Voice_AI_Agent

**Description:**  
This project is a voice assistant that interacts with a database and leverages Natural Language Processing techniques. The main objective is to receive voice commands, extract relevant information (entities and intentions), and then integrate with a database to facilitate lead, client, or business-relevant data management across various domains. You can have several questions, ask about the stored information by saying the lead codename. For more information on how the wizards work please refer to **src/README.md**.

---

### Dependency Installation

To install all dependencies required to run the assistant, copy and run the following command in your terminal:

```bash
pip install -r requirements.txt
```

---

## Frameworks / Stack Used

1. **Python 3.13.2**  
   - Programming language used.

2. **openai-agents[voice]**  
   - **OpenAI SDK:** open-source, lightweight. Used to build and orchestrate workflows between multiple agents.

3. **numpy**  
   - Everybody loves NumPy.

4. **sounddevice**  
   - For audio recording and playback using NumPy arrays.

5. **openai**  
   - Official OpenAI library to integrate models and services via their API.

6. **python-dotenv**  
   - Loads environment variables from `.env` files for secure configuration.  
     _(It’s recommended to create a local `.env` file during testing to store your OpenAI API key — and remember to exclude it in `.gitignore`)._

7. **transformers**  
   - Hugging Face’s Transformers library where we can use the amazing BERT and its family :).

8. **PySimpleGUI**  
   - GUI library for people who hate GUIs. Reading machine code is underrated :).

> **Note:** If you run into import issues with PySimpleGUI (e.g., missing `Text` module), try:
> ```bash
> pip install --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
> ```

---

## Project Structure

The main structure of the repository is as follows:

```
|-- Voice_AI_Agent
    |-- .gitignore
    |-- LICENSE
    |-- README.md
    |-- leads.db
    |-- requirements.txt
    |-- src (core logic)
    |   |-- config.py (environment variables loaded with `python-dotenv`)
    |   |-- ui_voice_assistant.py (GUI-integrated version)
    |   |-- voice_assistant.py (basic version: direct console interaction, no complex intent analysis)
    |   |-- voice_assistant_v1.py (intermediate version: console interaction, SQLite support, no complex intent analysis)
    |   |-- voice_assistant_v2.py (advanced version: console interaction, SQLite support, complex intent analysis using Hugging Face models)
    |   |-- agent
    |   |   |-- crm.py
    |   |   |-- crm_connector.py
    |   |   |-- crm_integration.py (CRM integration attempt — failed just like the others)
    |   |   |-- sqlite_db.py (Handles local `SQLite` DB interactions with `leads.db`)
    |   |-- nlp
    |   |   |-- entity_extraction.py (rudimentary extraction :()
    |   |   |-- entity_intention_extraction.py (logic to use models for text classification/sentiment analysis)
    |   |-- tests
    |   |-- api
    |       |-- __pycache__
    |-- .git
```

---

# ToDo

---

**1. Refactor the Code:**  
   - Create modular components for (audio processing, NLP, DB interaction) both in the GUI (PySimpleGUI) and in the rest of the assistant versions.

**2. Documentation:**  
   - Add usage examples in each module's README.  
   - Add specific documentation in the `docs/` folder (technologies, models, etc.).

**3. Caching, Contextual History, and Guardrails:**  
   - Create a cache system and guardrails to prevent irrelevant conversations.  
   - Run large-scale tests to analyze agent behavior with big data queries. Add more specific prompts to guide users.

**4. Interface and Data Base: Simple**  
   - Improve the interface and data base(use better stack) :), please.

**5. Testing:**  
   - Create more unit and integration tests.






