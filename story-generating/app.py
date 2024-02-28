from multiprocessing import AuthenticationError
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from openai import PermissionDeniedError, RateLimitError
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import json

load_dotenv(find_dotenv())

class Request(BaseModel):
    prompt: str 

def generate_story(scenario):
    template = """
    You are a story teller:
    You can generate a short story based on a simple narrative. The story should not be more than {ammount_words} words;
    """

    human_template = "{scenario}"
    chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

    messages = chat_prompt.format_messages(ammount_words=200, scenario=scenario)
    chat = ChatOpenAI(model='gpt-3.5-turbo')

    try:
        # story = chat.invoke(messages, max_tokens=200, temperature=0.7, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
        story = None
        with open("./example.json", 'r') as file:
            story = json.load(file)
        print(story)
        # return story.content
        return story['content']
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

app = FastAPI()

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=303)

@app.post("/generate")
async def generate(request: Request):
        try:
            story = generate_story(request.prompt)
            return {'result': 'success', 'story': story}
        except HTTPException as e:
            raise e

@app.get("/live")
async def live_endpoint():
    return {'status': 'Healthy'}

@app.get("/ready")
async def ready_endpoint():
    return {'status': 'Ready'}
