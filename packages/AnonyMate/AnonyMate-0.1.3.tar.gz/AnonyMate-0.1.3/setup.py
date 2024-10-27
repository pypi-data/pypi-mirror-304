from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='AnonyMate',
    version='0.1.3',
    description='A comprehensive toolkit for data anonymization, masking, and encryption.',
    long_description=long_description,  
    long_description_content_type='text/markdown',  
    author='Pasindu Bandara',
    author_email='pasindubandara99@gmail.com',
    url='https://github.com/PasinduBandaraa/AnonyMate',  
    packages=find_packages(include=["anonymate", "anonymate.*"]),
    install_requires=[
        'cryptography',
        'faker',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
