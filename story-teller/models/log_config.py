from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
log_level = os.getenv('LOG_LEVEL', 'INFO')

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "story-teller"
    LOG_FORMAT: str = "%(levelprefix)s %(message)s | %(asctime)s"
    LOG_LEVEL: str = log_level

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },

    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }