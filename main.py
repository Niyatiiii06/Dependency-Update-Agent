from agents.dependency_agent import dependency_agent
from storage.database import init_db, save_analysis

init_db()

if __name__ == "__main__":
    query = input("What dependency do you want to analyze? ")

    result = dependency_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": query,
            }
        ]
    })

    print("\nFINAL RESULT:\n")
    print(result["messages"][-1].content)