import os
import zipfile
import datetime
from pathlib import Path


def pack():
    # Configuration
    INCLUDED_FILES = ['requirements.txt', 'manage.py', 'caller.py']
    INCLUDED_DIRS = ['main_app', 'orm_skeleton', 'migrations']
    EXCLUDED_DIRS = ['__pycache__', '.git', '.vscode', '.idea', 'venv']

    # Remove old archives
    for item in os.listdir('.'):
        if item.endswith(".zip") and item.startswith("submission-"):
            os.remove(item)
            print(f"Removed old archive: {item}")

    # Create timestamp
    timestamp = datetime.datetime.now().strftime('%H-%M_%d.%m.%y')
    archive_name = f'submission-{timestamp}.zip'

    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

            current_dir = Path(root).name

            for file in files:
                file_path = Path(root) / file

                # Skip if it's in an excluded directory
                if any(excluded in str(file_path) for excluded in EXCLUDED_DIRS):
                    continue

                # Check if file should be included
                if (file in INCLUDED_FILES or
                        current_dir in INCLUDED_DIRS or
                        any(included_dir in str(file_path) for included_dir in INCLUDED_DIRS)):
                    archive_path = file_path.relative_to('.')
                    zipf.write(file_path, archive_path)
                    print(f"Added: {archive_path}")

    print(f'Submission created: {archive_name}')


if __name__ == '__main__':
    pack()