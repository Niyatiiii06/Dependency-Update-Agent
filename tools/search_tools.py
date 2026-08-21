from langchain_core.tools import tool

from search.hybrid_search import hybrid_search
from search.code_search import search_code


@tool
def search_changelog(package: str, query: str) -> list[str]:
    """Search changelog evidence for a package."""
    return hybrid_search(package, query)


@tool
def search_repository(repository_path: str, function_name: str) -> dict:
    """Search Python code for usage of a function or API."""
    return search_code(repository_path, function_name)