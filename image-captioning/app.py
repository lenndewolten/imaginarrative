from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch, requests, warnings, os
from dotenv import load_dotenv

class Options(BaseModel): 
    max_new_tokens: int = Field(None, ge=50, le=300)
    num_beams: int = Field(None, ge=1, le=10)
    num_return_sequences: int = Field(None, ge=1, le=10)
    early_stopping: bool = False
    temperature: float = Field(None, ge=0.0, le=1.0)
    do_sample: bool = None

class Request(BaseModel):
    image_url: str 
    image_text_input: str = Field(None)
    generate_options: Options = Field({})

load_dotenv()
model_path = os.getenv('CACHED_MODEL_PATH', 'models/Salesforce/blip-image-captioning-large')

def download_model():
    """Download a Hugging Face model and processor to the specified directory"""
    try:
        if not os.path.exists(model_path):
            os.makedirs(model_path)
    except FileExistsError:
        pass

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    model.save_pretrained(model_path)
    processor.save_pretrained(model_path)
    return model, processor

def get_model():
    model = None
    processor = None
    
    try:
        model = BlipForConditionalGeneration.from_pretrained(model_path)
        processor = BlipProcessor.from_pretrained(model_path)
    except Exception:
        model, processor = download_model()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return model, processor, device

model, processor, device = get_model()

app = FastAPI()

def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return Image.open(response.raw)
    else:
        raise Exception(f"Error downloading image from {url}. Status code: {response.status_code}")

def generate_captions(image_url, image_text_input, **kwargs):
    image = download_image(image_url)
    if image.mode != "RGB":
        image = image.convert(mode="RGB")
    
    inputs = processor(image, image_text_input, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, **kwargs)
    
    captions = []
    for sequence in outputs:
        caption = processor.decode(sequence, skip_special_tokens=True)
        captions.append({"generated_text": caption})
    
    return captions

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs", status_code=303)

@app.post("/image-captioning")
async def image_captioning_endpoint(request: Request):
    captured_warnings = []
    try:
        def capture_warnings(message, category, filename, lineno, file=None, line=None):
            warning_message = f"{message}"
            captured_warnings.append(warning_message)

        warnings.showwarning = capture_warnings
        warnings.simplefilter("always", UserWarning)

        captions = generate_captions(request.image_url, request.image_text_input, **vars(request.generate_options))
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
