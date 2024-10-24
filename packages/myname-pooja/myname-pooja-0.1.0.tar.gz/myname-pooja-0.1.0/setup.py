from setuptools import setup, find_packages

setup(
    name="myname-pooja",  # Package name
    version="0.1.0",  # Initial version
    description="A simple package for greeting functionality",  # Short description
    long_description=open("README.md").read(),  # Detailed description from README.md
    long_description_content_type="text/markdown",  # README file format
    author="Pooja Sambhwani",  # Your name
    author_email="pooja@example.com",  # Your email
    url="https://github.com/sambhwanipooja",  # URL to your project's repo (if any)
    packages=find_packages(),  # Automatically finds all packages
    classifiers=[  # PyPI classifiers
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
    install_requires=[],  # List of dependencies (if any)
)