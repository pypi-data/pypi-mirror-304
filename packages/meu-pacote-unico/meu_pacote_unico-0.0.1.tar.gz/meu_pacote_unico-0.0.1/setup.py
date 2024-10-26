from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="meu_pacote_unico",
    version="0.0.1",
    author="Johnnatan_Krause",
    author_email="johnnatankrause@gmail.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnnatanKrause/Desafio-04-DIO-Criando-um-Pacote-de-Processamento-de-Imagens-com-Python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)