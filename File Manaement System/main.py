from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime

# ==============================
# Metadata Class
# ==============================
class Metadata:
    def __init__(self, owner: str):
        self.owner = owner
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_timestamp(self):
        self.updated_at = datetime.now()


# ==============================
# Abstract FileEntity (File or Folder)
# ==============================
class FileEntity(ABC):
    def __init__(self, name: str, owner: str):
        self.name = name
        self.metadata = Metadata(owner)

    @abstractmethod
    def display(self, indent: int = 0):
        pass


# ==============================
# File Class
# ==============================
class File(FileEntity):
    def __init__(self, name: str, owner: str, content: str = ""):
        super().__init__(name, owner)
        # self.name = name
        # self.metadata = Metadata(owner)
        self.content = content

    def display(self, indent: int = 0):
        print("  " * indent + f"📄 {self.name} (Owner: {self.metadata.owner})")


# ==============================
# Folder Class
# Composite Pattern
# ==============================
class Folder(FileEntity):
    def __init__(self, name: str, owner: str):
        super().__init__(name, owner)
        self.children: Dict[str, FileEntity] = {}

    def add(self, entity: FileEntity):
        self.children[entity.name] = entity
        self.metadata.update_timestamp()

    def remove(self, name: str):
        if name in self.children:
            del self.children[name]
            self.metadata.update_timestamp()

    def get(self, name: str) -> Optional[FileEntity]:
        return self.children.get(name)

    def display(self, indent: int = 0):
        print("  " * indent + f"📁 {self.name}/ (Owner: {self.metadata.owner})")
        for child in self.children.values():
            child.display(indent + 1)


# ==============================
# StorageService (Uploader, Downloader, Deleter)
# Strategy-friendly wrapper (OCP, SRP)
# ==============================
class StorageService:
    def __init__(self, root: Folder):
        self.root = root

    def upload(self, path: List[str], file: File):
        current = self.root
        for folder_name in path:
            entity = current.get(folder_name)
            if isinstance(entity, Folder):
                current = entity
            else:
                raise Exception(f"Invalid path segment: {folder_name}")
        current.add(file)

    def download(self, path: List[str]) -> Optional[File]:
        current = self.root
        for i, name in enumerate(path):
            entity = current.get(name)
            if i == len(path) - 1:
                if isinstance(entity, File):
                    return entity
                else:
                    raise Exception("Path does not point to a file")
            if isinstance(entity, Folder):
                current = entity
            else:
                raise Exception(f"Invalid path segment: {name}")
        return None

    def delete(self, path: List[str]) -> bool:
        current = self.root
        for i, name in enumerate(path):
            if i == len(path) - 1:
                current.remove(name)
                return True
            entity = current.get(name)
            if isinstance(entity, Folder):
                current = entity
            else:
                raise Exception(f"Invalid path segment: {name}")
        return False


# ==============================
# DEMO
# ==============================
if __name__ == "__main__":
    root = Folder("root", "tushar")
    storage = StorageService(root)

    # Manually add folders
    work = Folder("work", "tushar")
    root.add(work)

    # Upload Files
    storage.upload(["work"], File("resume.pdf", "tushar", "This is Tushar's Resume"))
    storage.upload([], File("photo.png", "tushar", "Image data here"))

    # Display structure
    root.display()

    # Download
    file = storage.download(["work", "resume.pdf"])
    print("\n⬇️ Downloaded Content:", file.content)

    # Delete
    storage.delete(["photo.png"])
    print("\n🗑️ Deleted photo.png")

    # Display again
    print("\n📂 Updated Structure:")
    root.display()