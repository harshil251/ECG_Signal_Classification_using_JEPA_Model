import os
from pathlib import Path

def create_jepa_structure():
    # Define the directory and file structure
    structure = {
        "data": [],
        "models": ["__init__.py", "encoder.py", "predictor.py", "jepa_main.py"],
        "utils": ["__init__.py", "masking.py", "datasets.py"],
        "scripts": ["train.py", "evaluate.py"],
        "checkpoints": []
    }

    print("🚀 Starting JEPA project structure setup...")

    for folder, files in structure.items():
        # Create folder if it doesn't exist
        folder_path = Path(folder)
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {folder}/")
        else:
            print(f"✅ Directory already exists: {folder}/")

        # Create files inside the folder
        for file in files:
            file_path = folder_path / file
            if not file_path.exists():
                with open(file_path, "w") as f:
                    # Adding a basic header to the files
                    f.write(f'# {file} for JEPA project\n')
                print(f"  📄 Created file: {folder}/{file}")
            else:
                print(f"  ⚠️ File already exists: {folder}/{file}")

    # Create root level files if they don't exist
    root_files = [".gitignore", "README.md", "requirements.txt"]
    for rf in root_files:
        if not Path(rf).exists():
            with open(rf, "w") as f:
                if rf == ".gitignore":
                    f.write(".venv/\n__pycache__/\n*.pyc\ndata/\ncheckpoints/\n.DS_Store")
            print(f"📄 Created root file: {rf}")

    print("\n✨ Setup complete! You can now start coding.")

if __name__ == "__main__":
    create_jepa_structure()