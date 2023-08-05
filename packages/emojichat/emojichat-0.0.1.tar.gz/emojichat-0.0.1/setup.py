from __future__ import annotations

from setuptools import find_packages, setup

__version__ = "0.0.1"

install_requires = [
    "pytest",
    "pre-commit",
    "openai",
    "tqdm",
]

authors = "Zecheng Zhang"
emails = "zechengzhang97@gmail.com"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="emojichat",
    version=__version__,
    description="Chat with emojis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=authors,
    author_email=emails,
    keywords=[
        "emoji",
        "gpt",
        "chatgpt",
    ],
    python_requires=">=3.7",
    install_requires=install_requires,
    packages=find_packages(),
)
