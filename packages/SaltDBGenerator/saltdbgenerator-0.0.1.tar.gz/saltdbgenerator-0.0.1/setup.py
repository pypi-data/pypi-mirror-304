from setuptools import find_packages, setup

with open("readme.md", "r") as file:
    long_description = file.read()

setup(
    name="SaltDBGenerator",
    version="0.0.1",
    description="Best salt Generator for sqlite db",
    package={"": ""},
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamalice20/SaltDBGenerator",
    author="lamalice20",
    author_email="discord974a@gmail.com",
    install_requires=[""],
    python_requires=">=3.12.0",
)