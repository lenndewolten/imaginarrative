from transformers import BlipProcessor, BlipForConditionalGeneration
from dotenv import load_dotenv
import os

load_dotenv()
model_path = os.getenv('CACHED_MODEL_PATH', 'Salesforce/blip-image-captioning-large')

def download_model():
    """Download a Hugging Face model and processor to the specified directory"""
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    model.save_pretrained(model_path)
    processor.save_pretrained(model_path)

download_model()
