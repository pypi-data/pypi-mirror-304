from setuptools import setup, find_packages

setup(
    name="blikon_sdk",
    version="2.1.0",
    packages=find_packages(include=["blikon_sdk", "blikon_sdk.*"]),
    install_requires=[
        "fastapi==0.115.2",
        "pydantic-settings==2.6.0",
        "uvicorn==0.32.0",
        "python-jose==3.3.0",
        "httpx==0.13.3",
        "opencensus-ext-azure==1.1.13",
        "azure-identity==1.19.0,",
        "azure-keyvault-secrets==4.9.0",
        "deep-translator==1.11.4",
        "langdetect==1.0.9",
    ],
    description="Blikon SDK for security and middleware services",
    author="Raúl Díaz Peña",
    author_email="rdiaz@yosoyblueicon.com",
    license="BlikonⓇ",
    url="https://github.com/blikon/blikon_sdk",
)
