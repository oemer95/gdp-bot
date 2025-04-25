import os
import re
import getpass
from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from agent.tools.gdp_data import GDPData
from agent.tools.gdp_forecast import GDPForecaster
from agent.tools.gdp_plotter import GDPPlotter
from langchain.memory import ConversationBufferMemory


# OpenAI API key
if not os.environ.get("OPENAI_API_KEY"):
     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
# tools
gdp_data = GDPData()
forecast_tool = GDPForecaster()
plot_tool = GDPPlotter()

memory = ConversationBufferMemory(return_messages=True, output_key="output")

def parse_gdp_query(query: str):
    parts = [s.strip() for s in query.split(",")]
    if len(parts) != 2:
        return None, None
    country, year = parts
    try:
        return country, int(year)
    except ValueError:
        return None, None

def parse_gdp_compare_query(query: str):
    parts = [s.strip() for s in query.split(",")]
    if len(parts) < 2:
        return None, None
    *countries, year_str = parts
    try:
        year = int(year_str)
        return countries, year
    except ValueError:
        return None, None

tools = [
    Tool(
        name="GetGDP",
        func=lambda q: gdp_data.get_gdp(*parse_gdp_query(q)),
        description="Get the GDP of a country in a specific year, e.g. 'Germany, 2020'."
    ),
    Tool(
        name="CompareGDP",
        func=lambda q: gdp_data.compare_gdp(*parse_gdp_compare_query(q)),
        description="Compare the GDPs of multiple countries in a given year, e.g. 'Germany, France, Italy, 2020'."
    ),
    Tool(
        name="ForecastGDP", 
        func=lambda q: forecast_tool.forecast(*q.split(",")), 
        description="Forecast GDP of a country. Input e.g. 'Germany, 5' where 5 is the number of years to forecast."
    ),
    Tool(
        name="PlotGDP", 
        func=lambda q: plot_tool.plot(*[i.strip() if i.strip().isdigit() else i.strip() for i in q.split(",")]), 
        description="Plot GDP of a country over years, Input is a country name, a start year and an end year."
    ),
    Tool(
        name="EconomicOpinion",
        #func=lambda q: f"As an AI trained on GDP data, here's an answer: {q}",
        func=gdp_data.economic_opinion_tool_func,
        description="Provides an economic opinion on a country's GDP. Input should be a country name."
    ),
    Tool(
        name="PlotPreviousData",
        func=lambda q: plot_tool.plot_from_messages(memory, *q.split(",")),
        description="Plot GDP data that was mentioned in our previous conversation. Input: country name with optional start_year and end_year."
    )
]

#init llm and agent
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    memory=memory
)