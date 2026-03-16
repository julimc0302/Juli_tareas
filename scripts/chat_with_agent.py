import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.classification_agent import InsightsAgent
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env file.")
        return

    print("🤖 Welcome to the Peru GitHub Insights Agent CLI!")
    print("Type your questions about the ecosystem below. (Type 'exit' to quit)\n")
    
    agent = InsightsAgent()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye! 👋")
            break
            
        if not user_input.strip():
            continue
            
        print("\n🔍 Analyzing ecosystem data...")
        try:
            response = agent.answer_question(user_input)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
