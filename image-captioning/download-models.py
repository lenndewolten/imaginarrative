from transformers import BlipProcessor, BlipForConditionalGeneration
from dotenv import load_dotenv
import os

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

download_model()