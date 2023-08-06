from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ImtiazGermain",
    version="0.1.2",
    author="Aitzaz Imtiaz",
    author_email="aitzazimtiaz855@gmail.com",
    description="A Python library for checking if a number is a Imtiaz-Germain and Germain prime or not",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ImtiazGermain.readthedocs.io/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "sympy",
    ],
)
