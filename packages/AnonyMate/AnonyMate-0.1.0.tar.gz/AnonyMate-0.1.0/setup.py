from setuptools import setup, find_packages

setup(
    name='AnonyMate',  
    version='0.1.0', 
    description='A comprehensive toolkit for data anonymization, masking, and encryption.',
    author='Pasindu Bandara',
    author_email='pasindubandara99@gmail.com',
    url='https://github.com/yourusername/AnonyMate', 
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
