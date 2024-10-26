from setuptools import setup, find_packages

setup(
    name="Jikanapi",
    version="0.2.0",
    author="Praveen Senpai",
    author_email="pvnt20@gmail.com",
    description="A Python wrapper for the Jikan API for MyAnimeList.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/praveensenpai/Jikanapi",
    packages=find_packages(),
    install_requires=[
        "jikanpy",
        "pydantic",
        "rich",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
