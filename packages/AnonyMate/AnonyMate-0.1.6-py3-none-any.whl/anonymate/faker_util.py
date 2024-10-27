# anonymate/faker_util.py
from faker import Faker

fake = Faker()

def generate_fake_name() -> str:
    """Generate a fake name."""
    return fake.name()

def generate_fake_email() -> str:
    """Generate a fake email."""
    return fake.email()

def generate_fake_address() -> str:
    """Generate a fake address."""
    return fake.address()
