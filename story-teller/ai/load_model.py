from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan, GenerationConfig
import os, logging

logger = logging.getLogger("story-teller")

def download_processor(cache_path):
    try:
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
    except FileExistsError:
        pass
    
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    processor.save_pretrained(cache_path)
    return processor

def download_model(cache_path):
    try:
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
    except FileExistsError:
        pass
    
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    model.save_pretrained(cache_path, generation_config=GenerationConfig(max_length=1876))
    return model

def download_vocoder(cache_path):
    try:
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
    except FileExistsError:
        pass
    
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
    vocoder.save_pretrained(cache_path)
    return vocoder


def get_model(cache_path: str):
    model = None
    processor = None
    vocoder = None
    
    processor_path = f"{cache_path}/processor"
    model_path = f"{cache_path}/model"
    vocoder_path = f"{cache_path}/vocoder"
    try:
        logger.debug("Loading the model")
        processor = SpeechT5Processor.from_pretrained(processor_path)
        model = SpeechT5ForTextToSpeech.from_pretrained(model_path)
        vocoder = SpeechT5HifiGan.from_pretrained(vocoder_path)
        logger.debug("Model loaded from cache")
    except Exception:
        logger.debug("Model not found, downloading model")
        processor = download_processor(processor_path)
        model =download_model(model_path)
        vocoder = download_vocoder(vocoder_path)    
        logger.debug("Model downloaded")

    return model, processor, vocoder
