import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Debug prints to verify the paths
print("Project root directory:", project_root)
print("Current sys.path:", sys.path)

from src import create_app

print("create_app successfully imported:", create_app)

# Call the create_app function and run the application
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)