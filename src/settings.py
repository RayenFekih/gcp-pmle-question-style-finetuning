from logging.config import dictConfig
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.logger import LOGGING_CONFIG

# Setting up logging format and configuration for all scripts
dictConfig(LOGGING_CONFIG)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )
    INPUT_PATH = Path("data/gcp-ml-engineer.md")
    TRAIN_JSONL_PATH = Path("data/training_data.jsonl")
    METADATA_PATH = "data/metadata.jsonl"
    MODEL_NAME = "gemini-3.1-flash-lite"
    QUESTIONS_PATH = "data/training_data.jsonl"
    SFT_DATA_PATH = "data/sft_dataset.jsonl"

    # Fine-tuning hyperparameters
    MODEL_NAME: str = "unsloth/Qwen2.5-3B-Instruct"
    MAX_SEQ_LENGTH: int = 1024
    LORA_RANK: int = 64
    LEARNING_RATE: float = 5e-6
    LR_SCHEDULER_TYPE: str = "cosine"
    OPTIMIZER: str = "adamw_8bit"
    MAX_STEPS: int = 250


settings = Settings()
