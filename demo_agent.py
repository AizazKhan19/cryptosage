import asyncio

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
import streamlit as st
import dotenv
from google.adk.tools import google_search

dotenv.load_dotenv()

# defining simple agent that uses google search to answer questions

demo_agent = Agent(
    name = 'Demo_Agent',
    description = 'A simple agent that uses google search to answer questions.',
    model = "gemini-2.5-flash-lite",
    instruction = 'You are a helpful assistant that uses google search to answer questions. Use the google_search tool to find information and answer the user\'s question.',
    tools = [google_search]
)

runner = InMemoryRunner(demo_agent)

st.title("Demo Agent")
question = st.text_input("Ask a question:")

if question:
    runner = InMemoryRunner(demo_agent)
    response = asyncio.run(runner.run_debug(question))
    response_text = response[0].content.parts[0].text
    st.write(response_text)