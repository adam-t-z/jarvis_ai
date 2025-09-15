import os
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

load_dotenv()

# Initialize the LLM client once to reuse
llm = ChatOpenAI(
    model="mistralai/mistral-small-3.2-24b-instruct:free",
    base_url="https://openrouter.ai/api/v1/",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

async def run_browser_task(task: str):
    agent = Agent(
        task=task,
        llm=llm,
    )
    await agent.run(max_steps=5)
    return "Browser task completed."

def run_browser_task_sync(task: str):
    """Sync wrapper to call async browser task from sync code."""
    return asyncio.run(run_browser_task(task))
