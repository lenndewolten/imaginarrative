from transformers import VitsModel, AutoTokenizer
from fastapi.responses import RedirectResponse, FileResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, BackgroundTasks
from dotenv import load_dotenv
import os, uuid, logging
from logging.config import dictConfig
from config.log_config import LogConfig
from ai.load_model import get_model
from ai.load_embeddings import get_embeddings
import soundfile as sf

class RequestBody(BaseModel):
    text: str 

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("story-teller")

load_dotenv()
model_path = os.getenv('CACHED_MODEL_PATH', 'ai/models/microsoft/speecht5_tts')
embeddings_path = os.getenv('CACHED_EMBEDDINGS_PATH', 'ai/embeddings')


model, processor, vocoder = get_model(model_path)
speaker_embeddings = get_embeddings(embeddings_path)

app = FastAPI()

def clean_temp_audio_file(temp_audio_file):
    try:
        os.remove(temp_audio_file)
    except Exception as error:
            logger.error("Error removing temporary file: %s", error)

@app.post("/generate-speech")
def generated_audio(body: RequestBody, background_tasks: BackgroundTasks):
    try:
        text = body.text
        ## check if max 600
        inputs = processor(text=text, return_tensors="pt")

        temp_audio_file = f'{str(uuid.uuid4())}.wav'
        
        background_tasks.add_task(clean_temp_audio_file, temp_audio_file)

        logger.debug("Generating audio")
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        sf.write(temp_audio_file, speech.numpy(), samplerate=16000)
        logger.debug("Audio generated")

        return FileResponse(temp_audio_file, media_type='audio/wav')
    except Exception as e:
        raise HTTPException(500, str(e))
    
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=303)

@app.get("/live")
async def live_endpoint():
    return {'status': 'Healthy'}

@app.get("/ready")
async def ready_endpoint():
    return {'status': 'Ready'}