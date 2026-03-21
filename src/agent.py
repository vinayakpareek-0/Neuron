"""
    Neuron - AgentBuilder
    Creates the agent with tools, memory and prompt
"""

from langchain.agents import AgentExecutor , create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from src.config import llm , SYSTEM_PROMPT


def build_agent(tools: list)-> AgentExecutor:
    """Build the Neuron agent"""

    # prompt_template
    prompt = ChatPromptTemplate.from_messages([
        ("system",SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name ="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    # memory
    memory = ConversationBufferWindowMemory(
        k=10,
        memory_key = "chat_history",
        return_messages=True,
    )

    # agent
    agent= create_tool_calling_agent(llm , tools , prompt)

    # agent_executor

    return AgentExecutor(
        agent =agent , 
        tools =tools , 
        memory = memory,
        verbose = False,
        handle_parsing_errors =True,
    )
