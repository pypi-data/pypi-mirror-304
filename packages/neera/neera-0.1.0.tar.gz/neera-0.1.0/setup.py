from setuptools import setup, find_packages

setup(
    name="neera",  # Package name
    version="0.1.0",  # Initial version
    description="A simple package for greeting functionality",  # Short description
    long_description=open("README.md").read(),  # Long description from README.md
    long_description_content_type="text/markdown",
    author="Harsh Jain",  # Your name
    author_email="harsh@example.com",  # Your email
    url="https://github.com/harshjain/neera",  # Project URL, if applicable
    packages=find_packages(),  # Automatically finds packages in this directory
    classifiers=[  # Metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
    install_requires=[],  # Dependencies, can be empty if none
)



