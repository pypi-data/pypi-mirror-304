from setuptools import setup, find_packages
from os import path

work_dir = path.abspath(path.dirname(__file__))

with open(path.join(work_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ace_cookie_manager",
    version="0.0.1",
    description="A package to manage cookies in a web browser for Streamlit Apps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://analytics.sonova.com",
    author="ACE - Cem Bakar",
    author_email="cem.bakar@sonova.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
