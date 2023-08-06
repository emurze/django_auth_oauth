import os
from pathlib import Path
from .base import BASE_DIR

# from debug_toolbar.panels.logging import collector

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": os.getenv('LOGGING_LEVEL'),
            "class": "logging.FileHandler",
            "filename": Path(BASE_DIR.parent, "logs", "general.log"),
        },
        "stream": {
            "level": os.getenv('LOGGING_LEVEL'),
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "level": os.getenv('LOGGING_LEVEL'),
            "handlers": [
                "stream",
                "file",
            ],
            'propagate': True,
        },
    },
}
