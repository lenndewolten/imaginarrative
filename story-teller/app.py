from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, BackgroundTasks
from dotenv import load_dotenv
import os, uuid, logging
from logging.config import dictConfig
from config.log_config import LogConfig
from ai.load_model import get_model
from ai.load_embeddings import get_embeddings
import soundfile as sf
from fastapi.middleware.cors import CORSMiddleware

class RequestBody(BaseModel):
    text: str = Field(min_length=7, max_length=600)

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("story-teller")

load_dotenv()
model_path = os.getenv('CACHED_MODEL_PATH', 'ai/models/microsoft/speecht5_tts')
embeddings_path = os.getenv('CACHED_EMBEDDINGS_PATH', 'ai/embeddings')


model, processor, vocoder = get_model(model_path)
speaker_embeddings = get_embeddings(embeddings_path)

app = FastAPI(title="Story Teller", summary="This FastAPI application efficiently generates audio from input text using the pre-trained model 'microsoft/speecht5_tts', speaker embeddings, and a vocoder. The application processes input,  with a maximum text limit of 600 characters, using a dedicated processor. Upon completion, it delivers the synthesized audio as a WAV file (16,000 Hz) in response.")

allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = allowed_origins_str.split(",") if allowed_origins_str else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def clean_temp_audio_file(temp_audio_file):
    try:
        os.remove(temp_audio_file)
    except Exception as error:
            logger.error("Error removing temporary file: %s", error)

@app.post("/generate")
def generate_audio(body: RequestBody, background_tasks: BackgroundTasks):
    try:
        inputs = processor(text=body.text, return_tensors="pt")

        temp_audio_file = f'{str(uuid.uuid4())}.wav'
        background_tasks.add_task(clean_temp_audio_file, temp_audio_file)

        logger.debug("Generating audio")
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        sf.write(temp_audio_file, speech.numpy(), samplerate=16000)
        logger.debug("Audio generated")

        return FileResponse(temp_audio_file, media_type='audio/wav')
    except Exception as e:
        raise HTTPException(500, str(e))
    
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=303)

@app.get("/live")
async def live_endpoint():
    return {'status': 'Healthy'}

@app.get("/ready")
async def ready_endpoint():
    return {'status': 'Ready'}