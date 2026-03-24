"""
    Content drafter tool : drafts emails and social posts from a topic
    - PromptTemplate : reusable prompts with {variables}
    - PydanticOutputParser : forces llm o/p into a struct. pydantic model
    - LLMChain (via prompt | llm | parser) : chiaing components with a pipe operator
"""

from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from src.config import llm

class DraftOutput(BaseModel):
    title:str = Field(description="A catchy title for the context")
    content:str = Field(description="The main content of the draft")
    hashtags:list[str] = Field(description="List of a few relevant hashtags")

parser = PydanticOutputParser(pydantic_object= DraftOutput)

draft_prompt = PromptTemplate(
    input_variables=["content_type","topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()} ,
    template="""
    Draft a {content_type} about the following topic:
    Topic: {topic}
    Return the output in the following JSON format:
    {format_instructions}
    """
)

@tool
def draft_content(topic:str , content_type:str = "LinkedIn post")->str:
    """Draft a professional content (email , linkedIn post or tweet) about a topic.
    Provide 'topic' and optionally 'content_type' (default:LinkedIn post)"""

    # chain : prompt -> LLM -> parser (LCEL)
    chain = draft_prompt | llm | parser

    result = chain.invoke({"topic":topic , "content_type":content_type})

    output = f"##{result.title}\n\n{result.content}\n\n"
    output +="".join(result.hashtags)
    return output