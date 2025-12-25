from langgraph.graph import START , END ,StateGraph
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import os
import json
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
# from langchain_tavily import TavilySearchResults
import json
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
# llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", api_key=os.getenv("GEMINI_API_KEY"))

os.environ["TAVILY_API_KEY"]= os.getenv('TAVILY_API_KEY')


# search = TavilySearchResults(
#     max_results=5,
#     include_answer=True,      # optional: includes a quick summary
#     include_raw_content=True  # optional: includes full page snippets
# )

tools = [TavilySearch(
    max_results=5,
    include_answer=True,      # optional: includes a quick summary
    include_raw_content=True  # optional: includes full page snippets
)]




agent = create_agent(
    model=llm,
    tools=[TavilySearch(
        max_results=5,
        include_answer=True,
        include_raw_content=True
    )],

    system_prompt="You are a helpful assistant that can find news from Tavily.",
)

inputs = {"messages": [{"role": "user", "content": "query"}]}

class result(BaseModel):
    content : str
    source : str 
    link_of_news : str 


class State(BaseModel):
    query: str
    search_results: List[result]

def search_latest_news