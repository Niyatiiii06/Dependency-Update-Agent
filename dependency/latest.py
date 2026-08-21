import requests


def get_latest_version(package: str) -> str:
    response = requests.get(
        f"https://pypi.org/pypi/{package}/json",
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["info"]["version"]


if __name__ == "__main__":
    print(get_latest_version("packaging"))