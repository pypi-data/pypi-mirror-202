from setuptools import setup

setup(
    name="tdbug",
    version="1.0.7",
    author="Damon Pickett",
    description="A Python package which uses the OpenAI API to help developers in debugging.",
    packages=["tdbug"],
    install_requires=[
        "openai",
        "python-dotenv",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "tdbug=tdbug.main:main",
        ],
    },
    python_requires=">=3.7",
)
