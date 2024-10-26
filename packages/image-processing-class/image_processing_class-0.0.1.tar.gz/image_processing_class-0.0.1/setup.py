from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing-class",
    version="0.0.1",
    author="Rodolfo Almeida",
    author_email="rdfalmeida@protonmail.com",
    description="Class - Image processing. The original project belongs to Karina Tiemi Kato.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdfalmeida/image-processing-package.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.13',
)