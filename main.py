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


class Result(BaseModel):  # Assuming this is your result schema – adjust if needed
    title: str
    description: str
    url: str | None = None
    source: str | None = None

class llm_ans(BaseModel):
    search_results: List[Result]

class State(BaseModel):
    query: str
    search_results: List[Result]

def search_latest_news(state:State):
    query = state['query']
    inputs = {"messages": [{"role": "user", "content":query}]}
    result = agent.invoke(input)['message'][-1].content

    prpmpt = PromptTemplate(
        input_variables= {
            'result'
        },
        template= """
You are a helpful assistant that answers questions using search results.
Always respond **only** with valid JSON that matches this exact schema. Do not add any extra text, explanations, or markdown outside the JSON.

Schema (Pydantic model):
{
  "search_results": [
    {
      "title": "Short title of the result",
      "description": "A clear, concise summary or description of this result",
      "url": "The direct link to the source (or null if not available)",
      "source": "The name of the source (e.g., Forbes, NYT, Reuters) or null"
    },
    ...
  ]
}
Text to structure:
{result}
"""

    )
    llm_with_structure = llm.with_structured_output(llm_ans)
    final_result = llm_with_structure.invoke({
        'result ' : result
    })
    print(final_result)
    return {
        'search_results' : final_result
    }



graph = StateGraph(State)

graph.add_node('search_latest_news' , search_latest_news)
graph.add_edge(START,'search_latest_news')
graph.add_edge('search_latest_news',END)

workflow=graph.compile()



    





