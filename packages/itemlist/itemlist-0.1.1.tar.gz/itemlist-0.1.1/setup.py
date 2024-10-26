import sys
from setuptools import setup, find_packages

install_requires = []

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if sys.platform.startswith('win'):
    install_requires.append('windows-curses')

setup(
    name="itemlist",
    version="0.1.1",
    author="Haruki Nakajima",
    author_email="your.email@example.com",
    description="A CLI item selection and search library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Luftalian/itemlist",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'Sphinx>=3.2.1',
        'sphinx-autodoc-typehints>=1.11.0',
    ],
)
