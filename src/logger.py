import logging
import os
from datetime import datetime


# Create logs folder
os.makedirs("logs", exist_ok=True)


# Create daily log file
log_file = f"logs/validation_{datetime.now().strftime('%Y%m%d')}.log"


# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)