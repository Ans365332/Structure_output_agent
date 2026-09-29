from pydantic import BaseModel, Field


class QueryResponse(BaseModel):
    query: str = Field(
        description="The original user query"
    )

    answer: str = Field(
        description="A clear and accurate answer to the user's query"
    )

    key_points: list[str] = Field(
        description="Important points from the answer"
    )

    difficulty: str = Field(
        description="Difficulty level of the query: beginner, intermediate, or advanced"
    )