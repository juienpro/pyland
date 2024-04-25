import logging

logger = logging
logger.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pyland.log"),
        logging.StreamHandler()
    ]
)
    
