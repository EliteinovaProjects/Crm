import os
import shutil
from pathlib import Path
from typing import Optional


class StorageFactory:
    def __init__(self, base_path: str = "uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_file(self, file_content: bytes, filename: str, subfolder: str = "") -> str:
        folder_path = self.base_path / subfolder if subfolder else self.base_path
        folder_path.mkdir(parents=True, exist_ok=True)
        
        file_path = folder_path / filename
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        return str(file_path)

    def delete_file(self, file_path: str) -> bool:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    def get_file_url(self, file_path: str, base_url: str = "") -> str:
        relative_path = file_path.replace(str(self.base_path), "").lstrip("/\\")
        return f"{base_url}/uploads/{relative_path}"


storage = StorageFactory()
