from pathlib import Path
from packaging.requirements import Requirement

def parse_requirements(filepath: str) -> list[dict]:
    dependencies = []
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(filepath)

    with path.open(encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line or line.startswith("#"):
                continue

            try:
                req = Requirement(line)
            except Exception:
                continue

            specifier = str(req.specifier)

            dependencies.append({
                "name": req.name,
                "specifier": specifier,
                "exact_version": (
                    specifier[2:]
                    if specifier.startswith("==") and "," not in specifier
                    else None
                ),
                "extras": sorted(req.extras),
            })

    return dependencies