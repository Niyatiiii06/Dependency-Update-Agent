from langchain_core.tools import tool
from dependency.latest import get_latest_version
from dependency.version import compare


@tool
def check_version(package: str, current_version: str) -> dict:
    """Check whether a newer PyPI version exists for a package."""
    latest = get_latest_version(package)

    return {
        "package": package,
        "current": current_version,
        "latest": latest,
        "status": compare(current_version, latest),
    }