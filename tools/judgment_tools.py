from langchain_core.tools import tool

from judgment.judge import judge_impact
from storage.database import save_analysis


@tool
def assess_impact(
    package: str,
    current_version: str,
    target_version: str,
    changelog: list[str],
    code_usage: dict,
):
    """Assess whether a dependency update affects the project."""

    result = judge_impact(
        package,
        current_version,
        target_version,
        changelog,
        code_usage,
    )

    save_analysis({
        "package": package,
        "current_version": current_version,
        "target_version": target_version,
        "affected": result.affected,
        "impact": result.impact,
        "reason": result.reason,
        "recommendation": result.recommendation,
    })

    return result