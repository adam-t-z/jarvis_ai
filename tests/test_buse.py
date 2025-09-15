import asyncio
import os
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

load_dotenv()

# Configure the LLM with working model and endpoint
llm = ChatOpenAI(
    model="mistralai/mistral-small-3.2-24b-instruct:free",
    base_url="https://openrouter.ai/api/v1/",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Simple task: go to example.com and get the title of the page
agent = Agent(
    task="Go to example.com and give me the title of the page",
    llm=llm,
)

async def main():
    await agent.run(max_steps=5)
    print("Task finished")

asyncio.run(main())