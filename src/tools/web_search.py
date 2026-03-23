"""
Web Search Tool — wraps TavilySearchResults for the Neuron agent.
  - TavilySearchResults is a pre-built LangChain tool
  - Tool interface: has a .name, .description, and .run() method
"""

from langchain_community.tools.tavily_search import TavilySearchResults

search_tool = TavilySearchResults(
    max_results = 3,
    name= "web_search",
    description="Search the web for current information on any topic. Use this when the user asks about recent events, facts, or anything you're unsure about.",
)
