from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="firstpackage-upload",
    version="0.0.1",
    author="Andrew Mendes",
    author_email="reznort06@gmail.com",
    keywords='image processing',
    description="A simple package that I cloned from Digital Innovation One studying for data engineering with Python.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewgms2005/image-processing-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
