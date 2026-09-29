from src.agent import structured_query_agent


def test_parse_error_retry():

    result = structured_query_agent(
        user_query="What is Python?",
        max_retries=3,
        test_mode="parse_error"
    )

    assert "error" not in result

    assert result["query"] == "What is Python?"
    assert isinstance(result["answer"], str)
    assert isinstance(result["key_points"], list)
    assert result["difficulty"] in [
        "beginner",
        "intermediate",
        "advanced"
    ]


def test_validation_error_retry():

    result = structured_query_agent(
        user_query="What is Machine Learning?",
        max_retries=3,
        test_mode="validation_error"
    )

    assert "error" not in result

    assert result["query"] == "What is Machine Learning?"
    assert isinstance(result["answer"], str)
    assert isinstance(result["key_points"], list)
    assert result["difficulty"] in [
        "beginner",
        "intermediate",
        "advanced"
    ]