import pytest
from src.main import run_pipeline

def test_run_pipeline_basic():
    # Just ensure it runs without error
    user_prompt = "Test prompt about uniswap"
    outputs = run_pipeline(user_prompt)
    assert outputs is not None
