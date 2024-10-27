# tests/test_anonymizer.py
import pytest
from anonymate.anonymizer import Anonymizer

def test_mask_text():
    anonymizer = Anonymizer()
    assert anonymizer.mask_text("secret") == "******"

def test_hash_text():
    anonymizer = Anonymizer()
    hashed = anonymizer.hash_text("secret")
    assert len(hashed) == 64  # SHA-256 produces a 64-character hash

def test_encrypt_decrypt():
    anonymizer = Anonymizer()
    encrypted = anonymizer.encrypt_text("secret")
    decrypted = anonymizer.decrypt_text(encrypted)
    assert decrypted == "secret"
