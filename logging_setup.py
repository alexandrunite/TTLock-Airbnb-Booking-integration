import logging
from config import LOGGING_LEVEL, LOGGING_FILE

def setup_logging():
    logging.basicConfig(
        filename=LOGGING_FILE,
        level=getattr(logging, LOGGING_LEVEL.upper(), logging.INFO),
        format='%(asctime)s:%(levelname)s:%(message)s'
    )
