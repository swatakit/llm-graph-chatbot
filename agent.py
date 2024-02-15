from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from tools.vector import kg_qa
from tools.cypher import cypher_qa

from llm import llm

#For llm
def run_llm(query):
    results = llm.invoke(query)
    return results.content # this is for v1/chat/completion endpoint

# For kq_qa
def run_retriever(query):
    results = kg_qa.invoke(query)
    return results['result']

# For cypher_qa
def run_cypher(query):
    # return the whole AIMessage object and let the chain handle the response.
    return cypher_qa.invoke(query)

tools = [
    Tool.from_function(
        name="General Chat",
        description="For general chat about ICD code, disease, illness and health claim fraud patterns",
        func=run_llm,
        return_direct=True
    ),
    Tool.from_function(
        name="Vector Search Index", 
        description="Provides claims information based on claim's narration or claims's description using Vector Search",
        func = run_retriever, 
        return_direct=True
    ),
    Tool.from_function(
        name="Graph Cypher QA Chain",  
        description="Provides information about Customer, Claim, Claim Details like los(length of stay)/Disease/Risk, Agent, Hospital, Phone and Email in the claim database", 
        func = run_cypher,
        return_direct=False # force it as string
    ),
]

from langchain.chains.conversation.memory import ConversationBufferMemory
memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True,
)


# agent_prompt = hub.pull("hwchase17/react-chat")
agent_prompt = PromptTemplate.from_template("""
You are a claim handler expert providing information illness, symptom and claims
Be helpful and return as much information as possible.
Do not answer any questions that do not relate to illness, symptom and claims.
Do not answer any questions using your pre-trained knowledge, only use the information provided in the context.

TOOLS:
------

You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True
    )


