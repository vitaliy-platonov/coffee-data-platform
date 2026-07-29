
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


INITIAL_DATA_DIR = DATA_DIR / "initial"
INCREMENTAL_DATA_DIR = DATA_DIR / "incremental"
RAW_DATA_DIR = DATA_DIR / "raw"