import sys
import os

# Add the project directory to sys.path
sys.path.append(r"C:\Users\Julia\Downloads\sumer school\python\Tareas2\Juli_tareas")

from src.agents.classification_agent import InsightsAgent

def test_agent():
    print("--- Diagnostic: Testing InsightsAgent Summary ---")
    agent = InsightsAgent()
    summary = agent.get_ecosystem_summary()
    print("\nAGENT SUMMARY CONTENT:")
    print(summary)
    print("\n--- End of Diagnostic ---")

if __name__ == "__main__":
    test_agent()
