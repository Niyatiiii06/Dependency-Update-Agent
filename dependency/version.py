from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet

def satisfies(version: str, specifier: str) -> bool:
    try: #parsed_specifier                #parsed_version
        return SpecifierSet(specifier).contains(Version(version))
    except (InvalidVersion, ValueError) as e:
        raise ValueError(f"Invalid version/specifier: {version}, {specifier}") from e

def compare(current: str, target: str) -> str:
    try:
        current, target = Version(current), Version(target)
    except InvalidVersion as e:
        raise ValueError(f"Invalid version: {e}") from e

    if target > current:
        return "upgrade"
    if target < current:
        return "downgrade"
    return "same"

if __name__ == "__main__":
    print(satisfies("2.2.2", ">=1.5,<3"))
    print(compare("2.1.4", "2.2.0"))