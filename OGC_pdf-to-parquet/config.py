from pydantic import BaseModel
import os


class Settings(BaseModel):
    PARALLEL_INSTANCES: int = 40
    REQUESTS_PER_SECOND: int = 40
    GEMINI_MODEL: str = "openrouter/google/gemini-2.0-flash-lite-001"
    ZOOM_FACTOR: float = 1.5
    CHUNK_SIZE: int = 40
    INPUT_FOLDER: str = "Test"
    OUTPUT_FOLDER: str = "out_test"
    PARQUET_SIZE: int = 1420
    FILE_NAMES: str = "train"

    # env
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")


settings = Settings()
