from setuptools import setup, find_packages

setup(
    name="salik",  # Package name
    version="0.2.0",  # Incremented version; change as needed for new releases
    author="Salik Uddin",
    author_email="uddinsalik@outlook.com",
    description="A Python package to showcase Salik Uddin's professional portfolio",
    long_description=open("README.md").read(),  # Long description from README file
    long_description_content_type="text/markdown",  # Content type for long description
    url="https://github.com/salik03/salik",  # URL to the package's GitHub repository
    packages=find_packages(),  # Automatically find and include all packages
    classifiers=[
        "Programming Language :: Python :: 3",  # Supported Python versions
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",  # OS compatibility
        "Intended Audience :: Developers",  # Intended audience
        "Topic :: Software Development :: Libraries :: Python Modules",  # Package topic
    ],
    python_requires=">=3.6",  # Minimum required Python version
)
