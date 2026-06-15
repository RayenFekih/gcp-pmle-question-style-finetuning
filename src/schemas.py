from pydantic import BaseModel, Field


class QuestionMetadata(BaseModel):
    topic: str = Field(
        description="Broad PMLE topic tested by the question, such as MLOps, BigQuery ML, model serving, monitoring, security, or generative AI."
    )

    subtopic: str = Field(
        description="Specific concept or scenario tested by the question."
    )

    products: list[str] = Field(
        description="Google Cloud products, services, APIs, or tools involved in the question."
    )
