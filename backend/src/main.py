from fastapi import FastAPI
from backend.src.langchain.Chatbot import Chatbot
from backend.src.models.paper_rag_query import PaperQueryInput, PaperQueryOutput
from backend.src.utils.async_utils import async_retry

app = FastAPI(
    title="ML Research Paper Chatbot",
    description="Endpoints for RAG chatbot",
)

@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str):
    """Retry the agent if a tool fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    chatbot=Chatbot()
    return await chatbot.paper_agent_executor.ainvoke({"input": query})

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/paper-rag-agent")
async def query_paper_agent(query: PaperQueryInput) -> PaperQueryOutput:
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response