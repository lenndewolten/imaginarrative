from transformers import BlipProcessor, BlipForConditionalGeneration
import os, logging, torch

logger = logging.getLogger("image-captioning")

def download_model(model_path):
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

def get_model(model_path):
    model = None
    processor = None
    
    try:
        logger.debug("Loading the model")
        model = BlipForConditionalGeneration.from_pretrained(model_path)
        processor = BlipProcessor.from_pretrained(model_path)
        logger.debug("Model loaded from cache")
    except Exception:
        logger.debug("Model not found, downloading model")
        model, processor = download_model(model_path)
        logger.debug("Model downloaded")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return model, processor, device
