import sys
import os

# Add the project directory to sys.path
project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peru-github-users")
sys.path.append(project_dir)

# Import and run the main app
# Note: we import from app.main because peru-github-users is now in the path
from app.main import main

if __name__ == "__main__":
    main()
