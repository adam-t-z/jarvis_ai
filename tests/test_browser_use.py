# import asyncio
# import os

# from dotenv import load_dotenv

# from browser_use import Agent, ChatOpenAI

# load_dotenv()

# # All the models are type safe from OpenAI in case you need a list of supported models
# llm = ChatOpenAI(
# 	model='x-ai/grok-4',
# 	base_url='https://openrouter.ai/api/v1',
# 	api_key=os.getenv('OPENROUTER_API_KEY'),
# )
# agent = Agent(
# 	task='Go to example.com, click on the first link, and give me the title of the page',
# 	llm=llm,
# )


# async def main():
# 	await agent.run(max_steps=10)
# 	input('Press Enter to continue...')


# asyncio.run(main())

import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found")

async def query_openrouter():
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            "messages": [{"role": "user", "content": "What is the capital of Saudi?"}]
        }
        response = await client.post(API_URL, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        print(result['choices'][0]['message']['content'])

asyncio.run(query_openrouter())
