from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hu_city",
    version="1.0.0",
    author="Nagy Béla",
    author_email="nagy.belabudapest@gmail.com",
    description="Hungarian city names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kobanya/hu_city",
    py_modules=["hu_city"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
