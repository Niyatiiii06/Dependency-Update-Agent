from dependency.parser import parse_requirements
from dependency.version import compare, satisfies
from dependency.latest import get_latest_version


def check_dependency(dep: dict) -> dict:
    latest = get_latest_version(dep["name"])
    current = dep["exact_version"]

    if current is None:
        return {
            "name": dep["name"],
            "current": None,
            "latest": latest,
            "status": "current_version_unknown",
        }

    return {
        "name": dep["name"],
        "current": current,
        "latest": latest,
        "status": compare(current, latest),
        "latest_satisfies": (
            satisfies(latest, dep["specifier"])
            if dep["specifier"] else True
        ),
    }


if __name__ == "__main__":
    dependencies = parse_requirements(
        "sample_project/requirements.txt"
    )

    for dep in dependencies:
        print(check_dependency(dep))