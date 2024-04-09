from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from pydantic import BaseModel, Field, ValidationError
from fastapi.responses import RedirectResponse
from PIL import Image
from dotenv import load_dotenv
from logging.config import dictConfig
from config.log_config import LogConfig
from ai.load_model import get_model
import requests, warnings, os, logging
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI(title="Image Captioning", summary="This FastAPI application efficiently generates captions from input images using the pre-trained model 'Salesforce/blip-image-captioning-large'. The application processes input, with a maximum text limit of 600 characters, using a dedicated processor. Upon completion, it delivers the synthesized captions as a JSON response.")

allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = allowed_origins_str.split(",") if allowed_origins_str else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def download_image(url):
    logger.debug(f"Downloading image from {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        logger.debug(f"Image downloaded")
        return Image.open(response.raw)
    else:
        raise Exception(f"Error downloading image from {url}. Status code: {response.status_code}")

def generate_captions(image, image_text_input, **kwargs):
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

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=303)

@app.post("/generate-by-url")
async def image_captioning_endpoint_by_url(body: RequestBody):
    captured_warnings = []
    try:
        def capture_warnings(message, category, filename, lineno, file=None, line=None):
            warning_message = f"{message}"
            captured_warnings.append(warning_message)

        warnings.showwarning = capture_warnings
        warnings.simplefilter("always", UserWarning)

        image = download_image(body.image_url)
        captions = generate_captions(image, body.image_text_input, **vars(body.generate_options))
        return {'result': 'success', 'captions': captions, 'warnings': captured_warnings}
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        captured_warnings.clear()
        warnings.resetwarnings()

@app.post("/generate-by-file")
async def image_captioning_endpoint_by_file(file: UploadFile = File(), 
                                    image_text_input: str = Form(None), 
                                    max_new_tokens: int = Form(200),
                                    num_beams: int = Form(1),
                                    num_return_sequences: int = Form(1),
                                    early_stopping: bool = Form(False),
                                    temperature: float = Form(0.7),
                                    do_sample: bool = Form(False)):
    logger.debug(f"Processing file, {file.filename}")
    valid_extensions = ('.png', '.jpg', '.jpeg')
    if not any(file.filename.endswith(ext) for ext in valid_extensions):
        raise HTTPException(status_code=400, detail=f"Unsupported file extention, allowed extentions: {valid_extensions}")
    
    captured_warnings = []
    try:
        options = Options(
            max_new_tokens=max_new_tokens,
            num_beams=num_beams,
            num_return_sequences=num_return_sequences,
            early_stopping=early_stopping,
            temperature=temperature,
            do_sample=do_sample
        )
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        def capture_warnings(message, category, filename, lineno, file=None, line=None):
            warning_message = f"{message}"
            captured_warnings.append(warning_message)

        warnings.showwarning = capture_warnings
        warnings.simplefilter("always", UserWarning)

        captions = generate_captions(image, image_text_input, **vars(options))
        return {'result': 'success', 'captions': captions, 'warnings': captured_warnings}
    
    except ValidationError as e:
        print(e)
        raise HTTPException(status_code=400, detail=e.errors())
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
