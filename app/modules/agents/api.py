# app/modules/agents/api.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Initialize the APIRouter
router = APIRouter()

# Define the Pydantic models for the JSON outputs
class BlogTitle(BaseModel):
    title: str = Field(description="The recommended blog title.")
    strategy: str = Field(description="The strategy synopsis explaining how the title supports the campaign objectives.")

class BlogSuggestionOutput(BaseModel):
    titles: list[BlogTitle] = Field(description="List of recommended blog titles along with their strategy synopsis.")

class BlogSectionOutput(BaseModel):
    title: str = Field(description="The section title.")
    synopsis: str = Field(description="The synopsis of the section.")

class BlogContentItem(BaseModel):
    title: str = Field(description="The section title.")
    content: str = Field(description="The content of the section in the form of paragraphs.")

class BlogContentOutput(BaseModel):
    sections: list[BlogContentItem] = Field(description="List of sections with their titles and content.")

# Define the chains using JsonOutputParser and the specified format
# Blog Suggestion Chain
blog_suggestion_parser = JsonOutputParser(pydantic_object=BlogSuggestionOutput)
blog_suggestion_prompt = PromptTemplate(
    template="""
    Given the following campaign details:
    - Name: {campaign_name}
    - Description: {campaign_description}
    - Audience: {campaign_audience}
    - Purpose: {campaign_purpose}

    And the top-ranking content information from search results:
    {search_results}

    Please generate three blog title recommendations that align with the campaign goals.
    Additionally, provide a small strategy synopsis for each blog title suggested, explaining how it supports the campaign's objectives.
    {format_instructions}
    """,
    input_variables=["campaign_name", "campaign_description", "campaign_audience", "campaign_purpose", "search_results"],
    partial_variables={"format_instructions": blog_suggestion_parser.get_format_instructions()},
)
create_blog_suggestion_chain = blog_suggestion_prompt | ChatOpenAI(temperature=0.5) | blog_suggestion_parser

# Blog Section Chain
blog_section_parser = JsonOutputParser(pydantic_object=BlogSectionOutput)
blog_section_prompt = PromptTemplate(
    template="""
    You are a marketing content writer tasked with creating relevant sections of the Blog idea titled: {title}.
    In listing out the sections, consider the details provided in the Key Context section
    and ensure that the sections align with the campaign's objectives. Provide the Section heading and a brief explanation of the section's content.
    Consider the type of audience that will be reading the blog and to what aim for. 
    Do not make up any information, only use the information provided in the key context below.
    A typical blog post has multiple sections, each with a unique heading and content idea.
    An introductory section is usually the first section of a blog post, followed by the body sections and a conclusion.

    Key Context:
    - Blog Title: {title}
    - Synopsis: {synopsis}
    - Context: {context}
    - Campaign Name: {campaign_name}
    - Campaign Description: {campaign_description}
    - Campaign Audience: {campaign_audience}
    - Campaign Purpose: {campaign_purpose}

    {format_instructions}
    """,
    input_variables=["title", "synopsis", "context", "campaign_name", "campaign_description", "campaign_audience", "campaign_purpose"],
    partial_variables={"format_instructions": blog_section_parser.get_format_instructions()},
)
create_blog_section_chain = blog_section_prompt | ChatOpenAI(temperature=0.5) | blog_section_parser

# Blog Content Chain
blog_content_parser = JsonOutputParser(pydantic_object=BlogContentOutput)
blog_content_prompt = PromptTemplate(
    template="""
    You are a content writer tasked with creating detailed content for a blog post based on the following campaign details and list of sections identified below in the Key context area.
    Each section content can be between 1 to 5 paragraphs long as required. Ensure that the content is engaging, informative, and aligns with the campaign's objectives.
    Content should be written in a way that resonates with the target audience and supports the campaign's purpose.
    Use the context provide to guide the content creation process.
    The content being suggested should include annotations for items that require further clarification or additional information eg. [Citation Needed], [Example], [Statistic], [Reference Needed], etc.

    Key Context:
    - Campaign Name: {campaign_name}
    - Campaign Description: {campaign_description}
    - Campaign Audience: {campaign_audience}
    - Campaign Purpose: {campaign_purpose}

    Sections:
    {sections}

    For each section, provide the section title and content in the form of paragraphs.
    {format_instructions}
    """,
    input_variables=["campaign_name", "campaign_description", "campaign_audience", "campaign_purpose", "sections"],
    partial_variables={"format_instructions": blog_content_parser.get_format_instructions()},
)
create_blog_content_chain = blog_content_prompt | ChatOpenAI(temperature=0.3, max_tokens=4000, model="gpt-4o") | blog_content_parser

# Define request models
class BlogSuggestionRequest(BaseModel):
    campaign_name: str
    campaign_description: str
    campaign_audience: str
    campaign_purpose: str
    search_results: str

class BlogSectionRequest(BaseModel):
    title: str
    synopsis: str
    context: str
    campaign_name: str
    campaign_description: str
    campaign_audience: str
    campaign_purpose: str

class BlogSection(BaseModel):
    title: str
    synopsis: str

class BlogContentRequest(BaseModel):
    campaign_name: str
    campaign_description: str
    campaign_audience: str
    campaign_purpose: str
    sections: list[BlogSection]

class BlogSuggestionIDRequest(BaseModel):
    blog_suggestion_id: str

# Define routes for database operations
@router.get("/blogs/suggestions/{blog_suggestion_id}/details")
async def get_blog_suggestion(blog_suggestion_id: str):
    # TODO: Implement database retrieval logic
    try:
        # Placeholder for database retrieval logic
        return {"result": "Blog suggestion details retrieved from the database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/blogs/suggestions/list")
async def list_blog_suggestions():
    # TODO: Implement database listing logic
    try:
        # Placeholder for database listing logic
        return {"result": "List of blog suggestions retrieved from the database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/blogs/suggestions/{blog_suggestion_id}/delete")
async def delete_blog_suggestion(blog_suggestion_id: str):
    # TODO: Implement database deletion logic
    try:
        # Placeholder for database deletion logic
        return {"result": "Blog suggestion deleted from the database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export the chains for use in server.py
__all__ = [
    "create_blog_suggestion_chain",
    "create_blog_section_chain",
    "create_blog_content_chain",
    "router",
]
