# setup.py

from setuptools import setup, find_packages

setup(
    name="salik",
    version="0.1.0",
    author="Salik Uddin",
    author_email="uddinsalik@outlook.com",
    description="A package to display Salik Uddin's portfolio",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/salik03/salik",  # Link to GitHub repository
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
