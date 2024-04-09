from datasets import load_dataset, load_from_disk
import os, logging, torch

logger = logging.getLogger("story-teller")

def download_embeddings(model_path):
    """Download a Hugging Face model and processor to the specified directory"""
    try:
        if not os.path.exists(model_path):
            os.makedirs(model_path)
    except FileExistsError:
        pass

    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    embeddings_dataset.save_to_disk(model_path)
    return embeddings_dataset

def get_embeddings(cache_path: str):
    embeddings_dataset = None
    
    try:
        logger.debug("Loading the embeddings")
        embeddings_dataset = load_from_disk(cache_path)
        logger.debug("Embeddings loaded from cache")
    except Exception as e:
        logger.debug("Embeddings not found, downloading embeddings")
        embeddings_dataset = download_embeddings(cache_path)
        logger.debug("Embeddings downloaded")

    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
    return speaker_embeddings
