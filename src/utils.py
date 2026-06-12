import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
from google.genai.errors import ClientError
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from src.settings import settings

logger = logging.getLogger(__name__)

gemini_retry = retry(
    wait=wait_random_exponential(multiplier=1, max=60),
    stop=stop_after_attempt(7),
    retry=retry_if_exception_type(
        (ResourceExhausted, ServiceUnavailable, ClientError)),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)


def initialize_gemini_client():

    load_dotenv()

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    return client


def load_questions(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def already_processed_ids():
    ids = set()
    METADATA_FILE = Path(settings.METADATA_PATH)

    if not METADATA_FILE.exists():
        return ids

    with METADATA_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            ids.add(item["question_id"])

    return ids


def load_jsonl(path: Path) -> list[dict]:
    rows = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    return rows
