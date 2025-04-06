# Multiples-Agents

The voice assistant is structured as a multi-agent system comprising specialized agents:

## Example of 3 agents
- **Account Lead_Agent:**  
  Uses a custom tool (via the `function_tool` decorator) to provide account details based on a user ID.

- **Knowledge Lead_Agent:**  
  Employs the `FileSearchTool` to retrieve product information from a vector store, answering questions about all kind of products. What are the options for the user in the buisness/

- **Search Lead_Agent:**  
  Leverages the `WebSearchTool` to perform real-time web searches for up-to-date information.

A central **Triage Agent** receives the user’s query, determines the intent, and routes the request to the appropriate specialized agent. Importantly, every agent is configured to always respond in Spanish, ensuring a consistent language experience.

---

## Example Implementation

Below is an example of how to define the multi-agent along with its specialized agents:

```python
from agents import Agent, prompt_with_handoff_instructions
from my_custom_tools import get_account_info, WebSearchTool, FileSearchTool

# Specialized Agents
lead_agent = Agent(
    name="LeadAgent",
    instructions = voice_system_prompt + prompt_with_handoff_instructions("""
            You are a virtual assistant for qualifying and managing leads.
            Gather information and update the data base using:
            - 'parse_lead_info' to extract data.
            - 'update_crm' to add new leads.
            - 'update_lead_in_db' to modify fields of an existing lead.
            - 'delete_lead' to remove a lead by name.
            - 'list_all_leads' to list stored leads.
            Maintain a professional and friendly tone.
            Always respond in Spanish and slowly.
            """),
    model="gpt-4o",
    tools=[parse_lead_info, update_crm, update_lead_in_db, delete_lead, list_all_leads],
    output_type=str,
)

knowledge_agent = Agent(
    name="Knowledge_Lead_Agent",
    instructions=(
        "You answer user questions on our product portfolio with concise, helpful responses using the FileSearchTool. "
        "Always respond in Spanish."
    ),
    tools=[FileSearchTool(max_num_results=3, vector_store_ids=["VECTOR_STORE_ID"])],
)

search_agent = Agent(
    name="Search_Lead_Agent",
    instructions=(
        "You immediately provide an input to the WebSearchTool to find up-to-date information on the user's query. "
        "Always respond in Spanish."
    ),
    tools=[WebSearchTool()],
)

voice_system_prompt = """
[Output Structure]
Your output will be delivered in an audio voice response, please ensure that every response meets these guidelines:
1. Use a friendly, human tone that will sound natural when spoken aloud.
2. Keep responses short and segmented—ideally one to two concise sentences per step.
3. Avoid technical jargon; use plain language so that instructions are easy to understand.
4. Provide only essential details so as not to overwhelm the listener.
"""

# As a good practice we define the generic behavior for everyone
triage_agent = Agent(
    name="Ultimate_Lead_Agent",
    instructions=voice_system_prompt + prompt_with_handoff_instructions("""
You are the virtual assistant for Acme Shop. Welcome the user and ask how you can help.
Based on the user's intent, route the query to:
- AccountAgent for account-related inquiries,
- KnowledgeAgent for product FAQs,
- SearchAgent for real-time web search.
Always respond in Spanish.
"""),
    handoffs=[account_agent, knowledge_agent, search_agent],
)
```