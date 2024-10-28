from setuptools import setup, find_packages

setup(
    name="maskify-py",
    version="0.1.2",
    author="Raphael Augusto Ferroni Cardoso",
    author_email="rferronicardoso@gmail.com",
    description=(
        "Maskify is a lightweight, flexible library for Python, inspired by "
        "the Maskify.Core library for .NET. It helps developers securely mask "
        "sensitive data, such as Brazilian documents (CPF, CNPJ), emails, "
        "credit cards, and phone numbers. This library provides built-in "
        "masking for common data types, along with customizable masking options "
        "to ensure compliance with data protection regulations."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ninjapythonbrasil/maskify-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "numpy",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
        ],
    },
    package_data={
        "": ["*.txt", "*.md"],
    },
    entry_points={
        "console_scripts": [
            "mask = maskify.Masker:mask",
        ],
    },
)
