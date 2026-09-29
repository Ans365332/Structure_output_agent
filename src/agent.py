import os
import json

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from src.schemas import QueryResponse
from src.logger import logger


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"


def structured_query_agent(
    user_query: str,
    max_retries: int = 3,
    test_mode: str = None
):
    """
    Structured Output Agent

    Flow:
    User Query
        ↓
    LLM
        ↓
    JSON Parsing
        ↓
    Pydantic Validation
        ↓
    Success

    If error:
        ↓
    Log Error
        ↓
    Retry
        ↓
    Self Correction
    """

    last_error = None

    for attempt in range(1, max_retries + 1):

        try:

            # -----------------------------------------
            # SYSTEM PROMPT
            # -----------------------------------------

            system_prompt = """
You are a reliable AI assistant.

Answer the user's query and return ONLY valid JSON.

Required JSON structure:

{
    "query": "original user query",
    "answer": "clear and accurate answer",
    "key_points": [
        "important point 1",
        "important point 2"
    ],
    "difficulty": "beginner"
}

Rules:

1. query must contain the original user query.
2. answer must be clear and accurate.
3. key_points must be a list of strings.
4. difficulty must be exactly:
   beginner
   intermediate
   advanced
5. Do not add extra fields.
6. Return JSON only.
7. Do not use markdown.
8. Do not use ```json.

Technical context:

The user works with Data Science, Machine Learning,
GenAI, LLMs, RAG, Agents, APIs and MCP.

In this technical context, MCP means:
Model Context Protocol.
"""

            # -----------------------------------------
            # SELF-CORRECTION
            # -----------------------------------------

            if last_error:

                system_prompt += f"""

Your previous response failed.

Error:
{last_error}

Correct the mistake and return a completely valid
JSON response matching the required schema.

Return JSON only.
"""

            # -----------------------------------------
            # LLM CALL
            # -----------------------------------------

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
                ],
                temperature=0
            )

            raw_output = response.choices[0].message.content.strip()

            # -----------------------------------------
            # TEST: PARSE ERROR
            # -----------------------------------------

            if test_mode == "parse_error" and attempt == 1:

                raw_output = '{"query": "broken JSON"'

            # -----------------------------------------
            # JSON PARSING
            # -----------------------------------------

            try:

                data = json.loads(raw_output)

            except json.JSONDecodeError as e:

                error_message = (
                    f"Attempt {attempt} - "
                    f"JSON Parse Error: {e}"
                )

                logger.error(error_message)

                print(f"⚠️ {error_message}")

                last_error = error_message

                continue

            # -----------------------------------------
            # TEST: VALIDATION ERROR
            # -----------------------------------------

            if test_mode == "validation_error" and attempt == 1:

                # Intentionally remove required fields
                data = {
                    "query": user_query,
                    "answer": "Test answer"
                }

            # -----------------------------------------
            # PYDANTIC VALIDATION
            # -----------------------------------------

            try:

                validated_response = QueryResponse.model_validate(data)

                print(
                    f"✅ Validation successful "
                    f"on attempt {attempt}"
                )

                return validated_response.model_dump()

            except ValidationError as e:

                error_message = (
                    f"Attempt {attempt} - "
                    f"Pydantic Validation Error:\n{e}"
                )

                logger.error(error_message)

                print(
                    f"⚠️ Pydantic Validation Error "
                    f"on attempt {attempt}"
                )

                last_error = error_message

                continue

        except Exception as e:

            error_message = (
                f"Attempt {attempt} - "
                f"Unexpected Error: {e}"
            )

            logger.error(error_message)

            print(f"⚠️ Unexpected Error: {e}")

            last_error = error_message

            continue

    # -----------------------------------------
    # ALL RETRIES FAILED
    # -----------------------------------------

    logger.error(
        f"All {max_retries} attempts failed "
        f"for query: {user_query}"
    )

    return {
        "error": (
            f"Unable to generate valid response "
            f"after {max_retries} attempts."
        )
    }