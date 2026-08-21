from typing import Literal
from pydantic import BaseModel, Field
from langchain.agents import create_agent

from config.settings import model


class ImpactDecision(BaseModel):
    affected: bool = Field(description="Whether the update is likely to affect the project.")
    impact: Literal["low", "medium", "high"]
    reason: str
    recommendation: str


judge = create_agent(
    model=model,
    tools=[],
    system_prompt=(
        "You are a dependency impact analyst. "
        "Compare the changelog evidence directly with the code-search evidence. "
        "If the changelog explicitly says an API was removed and the code-search "
        "results show that API is used, mark affected=True and impact='high'. "
        "If the changelog explicitly says an API changed or was deprecated and the "
        "project uses it, mark the update at least medium impact. "
        "If no relevant code usage is found, mark affected=False unless the "
        "changelog indicates a broader project-wide breaking change. "
        "Do not invent evidence."
    ),
    response_format=ImpactDecision,
)


def judge_impact(package, current_version, target_version, changelog, code_usage):
    prompt = f"""
Package: {package}
Current version: {current_version}
Target version: {target_version}

Changelog evidence:
{changelog}

Code-search evidence:
{code_usage}

Decide whether the update affects this project.
"""

    result = judge.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })

    return result["structured_response"]