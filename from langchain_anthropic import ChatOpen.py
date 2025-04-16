from langchain_anthropic import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Create the agent

memory = MemorySaver()
model = ChatAnthropic(model_name = "claude-3-sonnet-20240229")
