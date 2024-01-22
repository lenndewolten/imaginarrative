from transformers import BlipProcessor, BlipForConditionalGeneration
import os

def download_model(model_path):
    """Download a Hugging Face model and processor to the specified directory"""
    if not os.path.exists(model_path):
        os.makedirs(model_path)

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    model.save_pretrained(model_path)
    processor.save_pretrained(model_path)

download_model('models/Salesforce/blip-image-captioning-large')
