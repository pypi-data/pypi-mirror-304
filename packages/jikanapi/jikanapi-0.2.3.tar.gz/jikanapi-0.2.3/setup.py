from setuptools import setup, find_packages

setup(
    name="Jikanapi",
    version="0.2.3",
    author="Praveen Senpai",
    author_email="pvnt20@gmail.com",
    description="A Python wrapper for the Jikan API for MyAnimeList.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/praveensenpai/Jikanapi",
    packages=find_packages(),
    install_requires=[
        "jikanpy-v4==1.0.2",
        "pydantic==2.9.2",
        "rich==13.9.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
