from setuptools import setup, find_packages

setup(
    name="maskify-py",
    version="0.1.0",
    author="Raphael Augusto Ferroni Cardoso",
    author_email="raphaelcardoso@outlook.com",
    description="Maskify is a lightweight, efficient, and flexible library designed to help developers securely mask sensitive data such as Brazilian documents (CPF, CNPJ), emails, credit cards, mobile and residential phones, and more. It provides out-of-the-box masking for common data types and customizable masking options for any other sensitive information, ensuring compliance with data protection regulations like LGPD.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ferronicardoso/maskify-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
