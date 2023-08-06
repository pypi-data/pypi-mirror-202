from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
with open(this_directory / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="universal_date_parser",
    version="0.0.2.1",
    author="Guangyu He",
    author_email="me@heguangyu.net",
    description="A universal date parser to parse any kind of (possible) date strings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guangyu-he/universal_date_parser",
    install_requires=[],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    tests_require=["pytest"]
)
