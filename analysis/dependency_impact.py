from search.hybrid_search import hybrid_search
from search.code_search import search_code
from judgment.judge import judge_impact


def analyze_dependency(
    repository_path: str,
    package: str,
    current_version: str,
    target_version: str,
    changelog_query: str,
    affected_api: str,
):
    changelog = hybrid_search(package, changelog_query)
    code_usage = search_code(repository_path, affected_api)

    return judge_impact(
        package,
        current_version,
        target_version,
        changelog,
        code_usage,
    )


if __name__ == "__main__":
    result = analyze_dependency(
        repository_path="sample_project",
        package="pandas",
        current_version="2.1.4",
        target_version="3.0.5",
        changelog_query="DataFrame.append removed breaking change migration",
        affected_api="append",
    )

    print(result)