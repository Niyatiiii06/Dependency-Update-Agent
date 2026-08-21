from langchain.agents import create_agent

from config.settings import model
from tools.dependency_tools import check_version
from tools.search_tools import search_changelog, search_repository
from tools.judgment_tools import assess_impact


dependency_agent = create_agent(
    model=model,
    tools=[
        check_version,
        search_changelog,
        search_repository,
        assess_impact,
    ],
    system_prompt=(
        "You are a dependency-update analysis agent.\n\n"

        "You MUST use the tools before giving a final verdict.\n\n"

        "Follow this workflow:\n"
        "1. Check the dependency's current and latest version.\n"
        "2. Search the changelog for breaking changes, removals, "
        "deprecations, and migration notes related to the update.\n"
        "3. Identify important APIs mentioned in the changelog.\n"
        "4. Search the repository for those APIs.\n"
        "5. Use the impact-assessment tool with the collected evidence.\n"
        "6. Base the final verdict on the tool evidence.\n\n"

        "Never claim an update is safe when the changelog explicitly "
        "shows that an API is removed or changed and the repository "
        "uses that API.\n"

        "Do not rely only on your own knowledge.\n"
        "Do not invent evidence.\n"
    ),
)