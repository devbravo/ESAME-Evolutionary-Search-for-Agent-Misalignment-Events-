from setuptools import setup, find_packages

setup(
    name="ESAME",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "python-dotenv",
        "langgraph-dev",
        "ipython"
    ],
)