import schedule
import time
from main import workflow 


def job():
    print("Running AI newsletter workflow...")
    workflow.invoke({
        'query' : "Give me the latest top 10 news and updates about AI, new open-source repositories, emerging technologies, LangChain, Retrieval-Augmented Generation (RAG), and other major advancements in the field. For each, provide a title, description, source, and link",
        'search_results': [],
        'email': "",
        'subject': "",
        'content': ""
    })

schedule.every(24).hours.do(job)

print("Scheduler started... Ctrl+C to stop")
while True:
    schedule.run_pending()
    time.sleep(60)
