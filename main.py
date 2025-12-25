import smtplib
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
import json
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import httpx
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
# llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))

os.environ["TAVILY_API_KEY"]= os.getenv('TAVILY_API_KEY')

agent = create_agent(
    model=llm,
    tools=[TavilySearch(
        max_results=10,
        include_answer=True,
        include_raw_content=True
    )],

    system_prompt="You are a helpful assistant that can find news from Tavily.",
)


class Result(BaseModel):
    title: str
    description: str
    url: str | None = None
    source: str | None = None

class llm_ans(BaseModel):
    search_results: List[Result]

class State(BaseModel):
    query: str
    search_results: List[Result]
    email : str 
    subject : str 
    content : str 

class mail(BaseModel):
    content : str 
    subject : str 

def search_latest_news(state:State)-> Dict:
    print("Inside search_latest_news")
    query = state.query
    input = {"messages": [{"role": "user", "content":query}]}
    result = agent.invoke(input)['messages'][-1].content
    # print(result)
    # print(type(result))

    prompt = PromptTemplate(
        input_variables= ["result"],
        template= """
You are a helpful assistant that answers questions using search results.
Always respond **only** with valid JSON that matches this exact schema. Do not add any extra text.

Schema (Pydantic model):
{{
  "search_results": [
    {{
      "title": "Short title of the result",
      "description": "A clear, concise summary or description of this result",
      "url": "The direct link to the source (or null if not available)",
      "source": "The name of the source (e.g., Forbes, NYT, Reuters) or null"
    }}
  ]
}}

Text to structure:
{result}
"""


    )

    llm_with_structure = llm.with_structured_output(llm_ans)
    chain = prompt | llm_with_structure 
    final_result = chain.invoke({"result": result})

    # print(final_result)
    return {
        'search_results' : final_result.search_results
    }

def send_mail(state: State) -> Dict:
    print("Inside send_mail")
    search_results = state.search_results
    print(search_results)
    receiver_email = os.getenv("RECEIVER_EMAIL")

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")


    prompt = PromptTemplate(
        input_variables=["news"],
        template="""
You are an expert newsletter writer and email UI designer.

Create a professional, visually appealing AI news email newsletter.

Rules:
- Output ONLY valid JSON
- Follow the schema exactly
- Email content must be HTML
- Use inline CSS only (email-safe)
- No JavaScript
- Mobile friendly
- Clean modern design

Newsletter requirements:
- Catchy subject line
- Header with logo or emoji (e.g. "🧠 Today's Top AI & Tech News") 
- Each news item in a card-style box with:
  - Title (bold, larger font) and must be  clickable 
  - Short description
  - Source (if available) always mandatory
  - Clickable link (button or styled link)
  - and do not do line clm there should be some widht but not full width for mobile view
- Subtle dividers between items
- Footer: "You are receiving this email because you subscribed to AI updates."
- Use modern fonts, colors, and padding for readability

News data:
{news}
"""
        
    )

    formatted_prompt = prompt.format(
        news=json.dumps(
            [item.model_dump() for item in search_results],
            indent=2
        )
    )

    llm_email = llm.with_structured_output(mail)
    email_result = llm_email.invoke(formatted_prompt)

    subject = email_result.subject
    html_content = email_result.content

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.attach(MIMEText(html_content, "html"))

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print(f"Email sent to {receiver_email}")

    return {
        "subject": subject,
        "content": html_content
    }


graph = StateGraph(State)

graph.add_node('search_latest_news' , search_latest_news)
graph.add_node('send_mail',send_mail)
graph.add_edge(START,'search_latest_news')
graph.add_edge('search_latest_news','send_mail')
graph.add_edge('send_mail',END)

workflow=graph.compile()

result = workflow.invoke({
    'query' : "Give me the latest top 10 news and updates about AI, new open-source repositories, emerging technologies, LangChain, Retrieval-Augmented Generation (RAG), and other major advancements in the field. For each, provide a title, description, source, and link",
    'search_results' : [],
    'email' : "",
    'subject' : "",
    'content' : ""
}
)


