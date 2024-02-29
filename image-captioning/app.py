from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
from PIL import Image
from dotenv import load_dotenv
from logging.config import dictConfig
from config.log_config import LogConfig
from ai.load_model import get_model
import requests, warnings, os, logging

class Options(BaseModel): 
    max_new_tokens: int = Field(200, ge=50, le=300)
    num_beams: int = Field(1, ge=1, le=10)
    num_return_sequences: int = Field(1, ge=1, le=10)
    early_stopping: bool = False
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    do_sample: bool = False

class RequestBody(BaseModel):
    image_url: str 
    image_text_input: str = Field(None)
    generate_options: Options = Field(Options())

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("image-captioning")

load_dotenv()
model_path = os.getenv('CACHED_MODEL_PATH', 'ai/models/Salesforce/blip-image-captioning-large')

model, processor, device = get_model(model_path)

app = FastAPI()

def download_image(url):
    logger.debug(f"Downloading image from {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        logger.debug(f"Image downloaded")
        return Image.open(response.raw)
    else:
        raise Exception(f"Error downloading image from {url}. Status code: {response.status_code}")

def generate_captions(image_url, image_text_input, **kwargs):
    image = download_image(image_url)
    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    
    logger.debug("Generating captions")
    inputs = processor(image, image_text_input, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, **kwargs)
    
    captions = []
    for sequence in outputs:
        caption = processor.decode(sequence, skip_special_tokens=True)
        captions.append({"generated_text": caption})
    
    logger.debug("Captions generated")
    return captions

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=303)

@app.post("/image-captioning")
async def image_captioning_endpoint(body: RequestBody):
    captured_warnings = []
    try:
        def capture_warnings(message, category, filename, lineno, file=None, line=None):
            warning_message = f"{message}"
            captured_warnings.append(warning_message)

        warnings.showwarning = capture_warnings
        warnings.simplefilter("always", UserWarning)

        captions = generate_captions(body.image_url, body.image_text_input, **vars(body.generate_options))
        return {'result': 'success', 'captions': captions, 'warnings': captured_warnings}
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        captured_warnings.clear()
        warnings.resetwarnings()

@app.get("/live")
async def live_endpoint():
    return {'status': 'Healthy'}

@app.get("/ready")
async def ready_endpoint():
    return {'status': 'Ready'}
