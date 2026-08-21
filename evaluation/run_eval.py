from agents.dependency_agent import dependency_agent
from storage.database import get_analyses, init_db
from evaluation.cases import CASES


def run_case(case):
    before = len(get_analyses())

    dependency_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": case["prompt"],
            }
        ]
    })

    rows = get_analyses()

    if len(rows) <= before:
        return None

    return rows[0]


def run_eval():
    init_db()

    passed = 0

    for i, case in enumerate(CASES, 1):
        print(f"\nRunning case {i}: {case['name']}")

        result = run_case(case)

        if result is None:
            print("FAIL: No database result")
            continue

        affected = bool(result[4])
        impact = result[5]

        passed_case = (
            affected == case["expected_affected"]
            and impact == case["expected_impact"]
        )

        if passed_case:
            passed += 1
            print("PASS")
        else:
            print("FAIL")
            print("Expected:", case["expected_affected"], case["expected_impact"])
            print("Actual:", affected, impact)

    accuracy = passed / len(CASES)

    print("\n" + "=" * 40)
    print(f"Passed: {passed}/{len(CASES)}")
    print(f"Accuracy: {accuracy:.0%}")


if __name__ == "__main__":
    run_eval()