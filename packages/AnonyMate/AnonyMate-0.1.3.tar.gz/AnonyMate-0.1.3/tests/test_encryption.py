# tests/test_encryption.py
from anonymate.encryption import generate_encryption_key, save_key_to_file, load_key_from_file

def test_generate_encryption_key():
    key = generate_encryption_key()
    assert isinstance(key, bytes)

def test_save_and_load_key():
    key = generate_encryption_key()
    save_key_to_file(key, "test_key.key")
    loaded_key = load_key_from_file("test_key.key")
    assert key == loaded_key
