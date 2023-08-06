import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-data-pomelo-bi",
    version="0.0.1",
    author="data owner",
    author_email="data@pomelo.la",
    description="Data cross lib packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pomelo-la/morbius-service",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)