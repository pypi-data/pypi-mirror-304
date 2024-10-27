# anonymate/encryption.py
from cryptography.fernet import Fernet

def generate_encryption_key() -> bytes:
    """Generate a new encryption key."""
    return Fernet.generate_key()

def load_key_from_file(file_path: str) -> bytes:
    """Load an encryption key from a file."""
    with open(file_path, 'rb') as file:
        return file.read()

def save_key_to_file(key: bytes, file_path: str):
    """Save an encryption key to a file."""
    with open(file_path, 'wb') as file:
        file.write(key)
