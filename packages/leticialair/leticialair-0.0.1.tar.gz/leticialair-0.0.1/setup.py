from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="leticialair",
    version="0.0.1",
    author="Letícia Lair",
    author_email="leticialair@hotmail.com",
    description="Pacote utilizado para dar get e put em diferentes tipos de arquivos no S3.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leticialair/leticialair-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
)
