import json
import re
from pathlib import Path

from google.genai import types
from tqdm import tqdm

from src.prompts import FIXED_TASK_PROMPT, SYSTEM_PROMPT, USER_PROMPT
from src.schemas import QuestionMetadata
from src.settings import settings
from src.utils import already_processed_ids, gemini_retry, initialize_gemini_client, load_jsonl, load_questions


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


@gemini_retry
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
            response_mime_type="application/json",
            response_schema=QuestionMetadata,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0
            ),
            temperature=temperature,
        ),
    )

    return response.parsed


def build_metadata():
    METADATA_FILE = Path(settings.METADATA_PATH)
    QUESTIONS_FILE = Path(settings.QUESTIONS_PATH)

    processed_ids = already_processed_ids()
    questions = load_questions(QUESTIONS_FILE)
    client = initialize_gemini_client()

    for row in tqdm(questions, ncols=200, desc="Processing questions"):
        question_id = row["question_id"]

        if question_id in processed_ids:
            continue

        try:
            metadata = extract_metadata(
                row, client, model=settings.MODEL_NAME, temperature=0.2)

            output_row = {
                "question_id": question_id,
                "topic_id": row["topic_id"],
                "metadata": metadata.model_dump(),
            }

            with METADATA_FILE.open("a", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        output_row,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        except Exception as e:
            print(
                f"Failed question {question_id}: {e}"
            )


def normalize_products(products: list[str]) -> list[str]:
    cleaned = []
    seen = set()

    for product in products:
        product = product.strip()

        if not product:
            continue

        key = product.lower()

        if key not in seen:
            cleaned.append(product)
            seen.add(key)

    return cleaned


def build_input(metadata: dict) -> str:
    products = normalize_products(metadata.get("products", []))
    product_text = "\n".join(f"- {product}" for product in products)

    base = (
        f"{FIXED_TASK_PROMPT}\n\n"
        f"Topic: {metadata['topic']}\n"
        f"Subtopic: {metadata['subtopic']}"
    )

    if product_text:
        base += f"\n\nProducts:\n{product_text}"

    return base


def clean_option_text(text: str) -> str:
    text = text.strip()

    text = re.sub(r"([a-zA-Z\)])(\d+\.)", r"\1 \2", text)
    text = re.sub(r"\.(\d+\.)", r". \1", text)
    text = re.sub(r"\s+", " ", text)

    return text


def build_output(question_row: dict) -> str:
    options = {
        k: clean_option_text(v)
        for k, v in question_row["options"].items()
    }

    return (
        f"Question:\n{question_row['question']}\n\n"
        f"A. {options['A']}\n"
        f"B. {options['B']}\n"
        f"C. {options['C']}\n"
        f"D. {options['D']}\n\n"
        f"Correct answer: {question_row['correct_answer']}"
    )


def generate_sft_data():
    questions = load_jsonl(Path(settings.QUESTIONS_PATH))
    metadata_rows = load_jsonl(Path(settings.METADATA_PATH))

    metadata_by_id = {
        row["question_id"]: row["metadata"]
        for row in metadata_rows
    }

    examples = []
    missing_metadata = 0

    for question_row in questions:
        question_id = question_row["question_id"]
        metadata = metadata_by_id.get(question_id)

        if metadata is None:
            missing_metadata += 1
            continue

        examples.append({
            "input": build_input(metadata),
            "output": build_output(question_row),
        })

    SFT_DATA_FILE = Path(settings.SFT_DATA_PATH)
    SFT_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with SFT_DATA_FILE.open("w", encoding="utf-8") as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
