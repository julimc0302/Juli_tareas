import sys
import subprocess

def main():
    print("🚀 Starting Streamlit Dashboard...")
    # Use sys.executable to ensure we use the same Python environment
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])

if __name__ == "__main__":
    main()
