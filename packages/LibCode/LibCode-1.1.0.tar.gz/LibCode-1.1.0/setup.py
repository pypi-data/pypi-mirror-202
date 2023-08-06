from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="LibCode",
    version="1.1.0",
    description="A data structures and algorithms library implemented with Python and tested with Pytest!",
    author="Axel Sanchez and  Mariia Podgaietska",
    packages=[
        "myLib",
    ],
    install_requires=[
        "pytest",
    ],
    license="MIT",
    url="https://github.com/Axeloooo/LibCode",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
