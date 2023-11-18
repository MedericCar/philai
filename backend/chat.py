from langchain.chat_models import ChatCohere
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_log_to_messages
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.tools.render import render_text_description
from langchain.tools import Tool

from prompt_io import load_prompt_template
from retriever import retrieval, retrieval_with_id


USER_PROMPT = load_prompt_template("prompts/user.txt")
TEMPLATE_TOOL_RESPONSE = load_prompt_template("prompts/tool_response.txt")


def get_prompt():
    input_variables = ["input", "chat_history", "agent_scratchpad", "tools", "tool_names"]

    messages = [
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template(USER_PROMPT),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]

    return ChatPromptTemplate(input_variables=input_variables, messages=messages)


def get_tools():
    return [
        Tool(
            name="Get most relevant projects for query",
            func=retrieval,
            description="Useful to retrieve relevant projects with regards to a text query."
        ),
            Tool(
            name="Get project information by UUID",
            func=retrieval_with_id,
            description="Useful to fetch information on a single project you know the UUID of."
        )
    ]


def get_chat_model_with_stop():
    chat_model = ChatCohere(temperature=0, model="command-nightly")
    chat_model_with_stop = chat_model.bind(stop=["\nObservation"])
    return chat_model_with_stop


def get_agent(chat_model_with_stop, tools, prompt):
    return (
        {
            "tools": lambda x: render_text_description(tools),
            "tool_names": lambda x: ", ".join([t.name for t in tools]),
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_messages(x["intermediate_steps"],
                                                                template_tool_response=TEMPLATE_TOOL_RESPONSE),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | chat_model_with_stop
        | JSONAgentOutputParser()
    )


def get_agent_executor():
    chat_model_with_stop = get_chat_model_with_stop()
    tools = get_tools()
    prompt = get_prompt()
    agent = get_agent(chat_model_with_stop, tools, prompt)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)