import json
import random
import re
from collections import Counter
from pathlib import Path

from google.genai import types

from src.prompts import SYSTEM_PROMPT, USER_PROMPT
from src.schemas import QuestionMetadata

INPUT_PATH = Path("data/gcp-ml-engineer.md")
TRAIN_JSONL_PATH = Path("data/training_data.jsonl")
METADATA_FILE = Path("data/metadata.jsonl")
MODEL_NAME = "gemini-3.1-flash-lite"


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_options(text: str) -> dict[str, str]:
    pattern = r"\n([A-D])\.\s+(.*?)(?=\n[A-D]\.\s+|\n\*\*Answer:|\Z)"
    matches = re.findall(pattern, text, flags=re.DOTALL)

    options = {}
    for letter, option_text in matches:
        options[letter] = clean_text(option_text)

    return options


def parse_block(block: str) -> dict | None:
    question_id_match = re.search(r"Question #:\s*(\d+)", block)
    topic_id_match = re.search(r"Topic #:\s*(\d+)", block)
    answer_match = re.search(r"\*\*Answer:\s*([A-D])\*\*", block)
    url_match = re.search(r"\[View on ExamTopics\]\((.*?)\)", block)
    timestamp_match = re.search(r"\*\*Timestamp:\s*(.*?)\*\*", block)

    if not question_id_match or not topic_id_match or not answer_match:
        return None

    question_id = int(question_id_match.group(1))
    topic_id = int(topic_id_match.group(1))
    correct_answer = answer_match.group(1)

    # Remove header/metadata before the real question
    question_part = block.split(
        "[All Professional Machine Learning Engineer Questions]", 1)
    if len(question_part) < 2:
        return None

    content = question_part[1]

    # Remove suggested answer line
    content = re.sub(r"Suggested Answer:\s*[A-D]\s*🗳️?", "", content)

    # Question text is before option A
    question_text_match = re.search(
        r"\n(.*?)(?=\nA\.\s+)", content, flags=re.DOTALL)
    if not question_text_match:
        return None

    question_text = clean_text(question_text_match.group(1))
    options = parse_options(content)

    if len(options) != 4:
        return None

    return {
        "question_id": question_id,
        "topic_id": topic_id,
        "question": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "timestamp": timestamp_match.group(1) if timestamp_match else None,
        "source_url": url_match.group(1) if url_match else None,
    }


def extract_metadata(question_row: dict, client, model: str, temperature: float = 0.2) -> QuestionMetadata:
    options = question_row["options"]
    user_prompt = USER_PROMPT.format(
        question=question_row["question"],
        option_a=options["A"],
        option_b=options["B"],
        option_c=options["C"],
        option_d=options["D"],
        correct_answer=question_row["correct_answer"],
    )

    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,

            # Structured output
            response_mime_type="application/json",
            response_schema=QuestionMetadata,

            # Disable thinking
            thinking_config=types.ThinkingConfig(
                thinking_budget=0
            ),

            temperature=temperature,
        ),
    )

    return response.parsed


def load_questions(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def already_processed_ids():
    ids = set()

    if not METADATA_FILE.exists():
        return ids

    with METADATA_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            ids.add(item["question_id"])

    return ids
