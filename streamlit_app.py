import sys
import os

# Add the project directory to sys.path so it can find the 'app' and 'src' packages
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main app
from app.main import main

if __name__ == "__main__":
    main()
