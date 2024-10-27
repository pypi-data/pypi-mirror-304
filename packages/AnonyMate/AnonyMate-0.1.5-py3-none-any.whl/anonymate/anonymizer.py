# anonymate/anonymizer.py
import hashlib
from cryptography.fernet import Fernet

class Anonymizer:
    def __init__(self, encryption_key: bytes = None):
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    def mask_text(self, text: str, mask_char: str = "*") -> str:
        """Mask the entire text with the specified character."""
        return mask_char * len(text)

    def hash_text(self, text: str) -> str:
        """Hash the text using SHA-256."""
        return hashlib.sha256(text.encode()).hexdigest()

    def encrypt_text(self, text: str) -> str:
        """Encrypt text, returning the encoded result."""
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt_text(self, encrypted_text: str) -> str:
        """Decrypt the encrypted text, returning the original value."""
        return self.cipher.decrypt(encrypted_text.encode()).decode()
