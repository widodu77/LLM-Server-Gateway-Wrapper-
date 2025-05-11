from setuptools import setup, find_packages

setup(
    name="llmops-gateway",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "httpx",
        "pytest",
        "pytest-asyncio",
        "python-dotenv",
        "pydantic",
        "pydantic-settings"
    ],
) 