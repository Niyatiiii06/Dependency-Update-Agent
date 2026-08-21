CASES = [
    {
        "name": "Removed API in use",
        "prompt": (
            "Analyze the pandas update from 2.1.4 to 3.0.5 in "
            "sample_project. The changelog explicitly states that "
            "DataFrame.append() was removed. Search the repository for "
            "append usage and determine whether the update affects the project."
        ),
        "expected_affected": True,
        "expected_impact": "high",
    },
    {
        "name": "Removed API not used",
        "prompt": (
            "Analyze the pandas update from 2.1.4 to 3.0.5 in "
            "sample_project. Check whether Series.append is affected."
        ),
        "expected_affected": False,
        "expected_impact": "low",
    },
    {
        "name": "Unused indexing API",
        "prompt": (
            "Analyze the pandas update from 2.1.4 to 3.0.5 in "
            "sample_project. Check whether pandas legacy indexing APIs "
            "are used and whether they affect the update."
        ),
        "expected_affected": False,
        "expected_impact": "low",
    },
    {
        "name": "Unused groupby API",
        "prompt": (
            "Analyze the pandas update from 2.1.4 to 3.0.5 in "
            "sample_project. Check whether groupby-related breaking "
            "changes affect the repository."
        ),
        "expected_affected": False,
        "expected_impact": "low",
    },
    {
        "name": "Unused API",
        "prompt": (
            "Analyze the pandas update from 2.1.4 to 3.0.5 in "
            "sample_project. Check whether a nonexistent pandas API "
            "called fake_removed_api affects the repository."
        ),
        "expected_affected": False,
        "expected_impact": "low",
    },
]