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
        "Use the changelog evidence and code-search evidence to decide "
        "whether a dependency update is likely to affect the project. "
        "Do not invent evidence. "
        "If no relevant code usage is found, do not claim the project is affected."
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