from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="many-toon-cli",
    version="0.1.3",
    description="A CLI tool for interacting with manga sites asynchronously and downloading 18+ manhwa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="hasanfq",
    author_email="hasanfq818@gmail.com",
    url="https://github.com/Kamanati/many-toon-cli",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.9.3",
        "tqdm>=4.62.3",
        "pillow>=8.3.1",
        "fpdf>=1.7.2",
        "argparse>=1.4.0",
    ],
    entry_points={
        "console_scripts": [
            "many-toon-cli=many_toons_cli.manga",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 
