from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ez-bar",
    version="0.1.2",
    author="kadir-karagoz",
    author_email="kadir@kadirkaragoz.com",
    description="Simple progress bar for terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kdrkrgz/ez-bar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
