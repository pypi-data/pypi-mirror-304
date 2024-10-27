from setuptools import setup, find_packages

setup(
    name="pydplyr",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    author="Nabin Oli",
    author_email="nabinoli2004@gmail.com",
    description="Syntax of dplyr in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nabin2004/pydplyr",
    classifiers=[
        "Programming Language :: Python",
    ],
    python_requires='>=3.6',
)