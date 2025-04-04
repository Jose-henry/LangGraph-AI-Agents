from setuptools import setup, find_packages

setup(
    name="rag",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "langchain",
        "langchain-openai",
        "pinecone-client",
        "python-dotenv",
    ],
) 