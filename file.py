import os

def create_project_structure(root_path):
    # Define the structure: Keys are folder paths, values are lists of files
    structure = {
        ".": ["README.md", "requirements.txt", ".env", "config.py"],
        "data/raw": ["price_log.csv"],
        "data/processed": [],
        "data/models": [],
        "scraper": ["__init__.py", "fetch_price.py", "parser.py", "utils.py"],
        "database": ["__init__.py", "db.py", "schema.sql"],
        "ml": ["__init__.py", "preprocess.py", "train_model.py", "predict.py", "decision.py"],
        "scheduler": ["__init__.py", "job_runner.py"],
        "dashboard": ["__init__.py", "app.py"],
        "notebooks": ["analysis.ipynb"],
        "tests": ["test_scraper.py", "test_model.py", "test_utils.py"]
    }

    print(f"Creating project structure in: {root_path}")

    for folder, files in structure.items():
        # Create the full directory path
        target_dir = os.path.join(root_path, folder)
        os.makedirs(target_dir, exist_ok=True)
        
        for file in files:
            file_path = os.path.join(target_dir, file)
            # Create an empty file if it doesn't exist
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    pass
                print(f"Created: {file_path}")
            else:
                print(f"Skipped (exists): {file_path}")

if __name__ == "__main__":
    # Your specific path
    target_folder = r"C:\Users\Mahi Patel\OneDrive\Desktop\PYTHONCIAP\price-watch-ai"
    
    create_project_structure(target_folder)
    print("\nProject structure created successfully!")