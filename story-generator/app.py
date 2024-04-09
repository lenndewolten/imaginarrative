from multiprocessing import AuthenticationError
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from openai import PermissionDeniedError, RateLimitError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(find_dotenv())

class Options(BaseModel): 
    max_characters: int = Field(500, ge=100, le=600)
    max_tokens: int = Field(258, ge=100, le=300)

class Request(BaseModel):
    prompt: str
    options: Options = Field(Options())

def generate_story(scenario: str, options: Options):
    template = """
    You are a story teller:
    You can generate a short story based on a simple narrative. The story MUST not be more than {max_characters} characters long.;
    """

    human_template = "{scenario}"
    chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

    messages = chat_prompt.format_messages(max_characters=options.max_characters, scenario=scenario)
    chat = ChatOpenAI(model='gpt-3.5-turbo')

    try:
        story = chat.invoke(messages, max_tokens=options.max_tokens, temperature=0.7, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
        return story.content
    except RateLimitError or AuthenticationError or PermissionDeniedError as e:
        error_message = e.body['message']

        raise HTTPException(e.status_code, error_message)

    except Exception as e:
        status_code = 500
        error_message = f"An error occurred while processing the request: {e}"
        if hasattr(e, 'status_code'):
            status_code = e.status_code

        if hasattr(e, 'body') and 'message' in e.body:
            error_message = e.body['message']
        
        raise HTTPException(status_code, error_message)

app = FastAPI(title="Story Generator", summary="The Story Generator API is a creative tool that leverages the power of OpenAI's GPT-3.5-turbo model to craft engaging short stories based on user-provided prompts. Whether you're looking for a quick narrative or seeking inspiration, this API transforms your ideas into captivating tales.")

allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = allowed_origins_str.split(",") if allowed_origins_str else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=303)

@app.post("/generate")
async def generate(request: Request):
        try:
            story = generate_story(request.prompt, request.options)
            return {'result': 'success', 'story': story}
        except HTTPException as e:
            raise e

@app.get("/live")
async def live_endpoint():
    return {'status': 'Healthy'}

@app.get("/ready")
async def ready_endpoint():
    return {'status': 'Ready'}
