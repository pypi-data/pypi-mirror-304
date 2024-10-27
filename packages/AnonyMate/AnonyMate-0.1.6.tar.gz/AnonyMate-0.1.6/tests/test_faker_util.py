# tests/test_faker_util.py
from anonymate.faker_util import generate_fake_name, generate_fake_email, generate_fake_address

def test_generate_fake_name():
    assert isinstance(generate_fake_name(), str)

def test_generate_fake_email():
    assert "@" in generate_fake_email()

def test_generate_fake_address():
    assert isinstance(generate_fake_address(), str)
