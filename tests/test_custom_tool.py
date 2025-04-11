import pytest
from portia.tool import ToolRunContext
from src.custom_tool import CustomTool

def test_custom_tool_runs():
    tool = CustomTool()
    ctx = ToolRunContext(
        execution_context=None,
        plan_run_id=None,
        config=None,
        clarifications=[]
    )
    result = tool.run(ctx)
    assert result == "Placeholder result from custom tool"
