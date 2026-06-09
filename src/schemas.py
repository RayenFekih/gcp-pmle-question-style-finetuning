from typing import Literal

from pydantic import BaseModel, Field


class QuestionMetadata(BaseModel):
    topic: str = Field(
        description="Main PMLE topic tested by the question"
    )

    exam_objective: str = Field(
        description="Exam competency being assessed"
    )

    difficulty: Literal["easy", "medium", "hard"] = Field(
        description="Difficulty level of the question. easy, medium, or hard"
    )

    trap_type: str = Field(
        description="Primary exam trap or distractor pattern"
    )

    topic_notes: list[str] = Field(
        description="3-6 concise notes describing the scenario without revealing the answer"
    )

    key_constraints: list[str] = Field(
        description="Important constraints that influence the correct decision"
    )
