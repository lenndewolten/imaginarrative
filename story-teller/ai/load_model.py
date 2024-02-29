from transformers import VitsModel, AutoTokenizer

import os, logging

logger = logging.getLogger("story-teller")

def download_model(model_path):
    """Download a Hugging Face model and processor to the specified directory"""
    try:
        if not os.path.exists(model_path):
            os.makedirs(model_path)
    except FileExistsError:
        pass

    model = VitsModel.from_pretrained("facebook/mms-tts-eng")
    tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    return model, tokenizer

def get_model(model_path: str):
    model = None
    tokenizer = None
    
    try:
        logger.debug("Loading the model")
        model = VitsModel.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        logger.debug("Model loaded from cache")
    except Exception:
        logger.debug("Model not found, downloading model")
        model, tokenizer = download_model(model_path)
        logger.debug("Model downloaded")

    return model, tokenizer
