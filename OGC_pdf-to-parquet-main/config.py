# config.py

from dotenv import load_dotenv
import os



load_dotenv(override=True)



# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Rate Settings
PARALLEL_INSTANCES = 5
REQUESTS_PER_SECOND = 2
MAX_RETRIES = 3
RETRY_BACKOFF = 5

# Model Settings
GEMINI_MODEL = "gemini/gemini-1.5-flash"

# Image Settings
ZOOM_FACTOR = 1.5
CHUNK_SIZE = 5
OUTPUT_FORMAT = "jpeg"

# Files settings
INPUT_FOLDER = "Test"
OUTPUT_FOLDER = "out_test"
PARQUET_SIZE = 50
FILE_NAMES = "train"  # train or test split ?